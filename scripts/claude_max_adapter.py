"""Claude-Max adapter: a local Anthropic-Messages-API lookalike backed by the
Claude Code CLI (authenticated against the user's Max plan).

Purpose: lets tools that expect a raw ANTHROPIC_API_KEY (here: Pol.is's delphi
service, patched to honour ANTHROPIC_BASE_URL) run their LLM calls through the
user's own logged-in `claude` CLI instead of a paid API key.

Scope & honesty: LOCAL DEV/DEMO USE. The sanctioned programmatic surface of a
Max plan is Claude Code / the Agent SDK — which is exactly what executes each
request here. For anything public or production, use a real API key.

Endpoints:
  POST /v1/messages        -> runs `claude -p --output-format json` per request
  POST /v1/messages/batch  -> 404 on purpose (delphi then falls back to
                              sequential /v1/messages calls)

Run:  python scripts/claude_max_adapter.py   (listens on 0.0.0.0:8787)
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8787
# Bind loopback only. Docker Desktop routes container->host via the special
# host-gateway address, which maps to the host loopback — so the delphi
# container reaches this at host.docker.internal:8787 WITHOUT exposing an
# arbitrary-prompt RCE endpoint to the wider local network.
HOST = "127.0.0.1"
# Path to the Claude Code CLI; set CLAUDE_BIN if it is not on PATH.
CLAUDE = os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "claude"
CALL_TIMEOUT_S = 420


def run_claude(prompt: str, system: str | None, model: str | None) -> dict:
    """Execute one prompt through the Claude Code CLI; return Anthropic-shaped message.

    The app's system prompt is passed via --system-prompt (which REPLACES Claude
    Code's default agent persona), so an arbitrary "become X, output only JSON"
    instruction is honoured as a legitimate system prompt instead of tripping
    Claude Code's prompt-injection defences when smuggled inside user content.
    """
    cmd = [CLAUDE, "-p", "--output-format", "json"]
    if system:
        cmd += ["--system-prompt", system]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    proc = subprocess.run(
        cmd, input=prompt.encode("utf-8"),
        capture_output=True, timeout=CALL_TIMEOUT_S,
    )
    out = proc.stdout.decode("utf-8", errors="replace").strip()
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI exit {proc.returncode}: {proc.stderr.decode(errors='replace')[:400]}")
    try:
        envelope = json.loads(out)
        text = envelope.get("result", out)
        usage = envelope.get("usage", {}) or {}
    except json.JSONDecodeError:
        text, usage = out, {}
    print(f"  [claude] {len(prompt)} chars in -> {len(text)} chars out in {time.time()-t0:.1f}s", flush=True)
    return {
        "id": f"msg_{uuid.uuid4().hex[:16]}",
        "type": "message",
        "role": "assistant",
        "model": model or "claude",
        "content": [{"type": "text", "text": text}],
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "usage": {
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
        },
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quieter default logging
        print(f"[{self.address_string()}] {fmt % args}", flush=True)

    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        if self.path.rstrip("/") == "/v1/messages":
            try:
                req = json.loads(raw)
                system = req.get("system") or ""
                user_parts = []
                for m in req.get("messages", []):
                    content = m.get("content")
                    if isinstance(content, list):
                        content = "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
                    user_parts.append(str(content))
                prompt = "\n\n".join(user_parts)
                self._send(200, run_claude(prompt, system or None, req.get("model")))
            except Exception as e:
                self._send(500, {"type": "error", "error": {"type": "api_error", "message": str(e)[:500]}})
        elif "batch" in self.path:
            # deliberate 404: delphi treats this as "Batch API unavailable"
            # and falls back to sequential /v1/messages calls.
            self._send(404, {"type": "error", "error": {"type": "not_found_error", "message": "batch not supported by local adapter"}})
        else:
            self._send(404, {"type": "error", "error": {"type": "not_found_error", "message": self.path}})


if __name__ == "__main__":
    print(f"claude-max adapter on {HOST}:{PORT}  (cli: {CLAUDE})", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
