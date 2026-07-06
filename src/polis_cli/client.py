"""HTTP client for Pol.is-family instances.

Arm's-length rule: this module speaks HTTP to an UNMODIFIED Pol.is/Voxit
instance. It contains no Pol.is code. Endpoint map written against the
`stable` branch (mid-2026); older/newer instances may differ — profiles
pin the version.

Auth flavors:
  * password — legacy POST /api/v3/auth/login {email, password} -> cookie
    session + xsrf token (present on stable/older instances; likely Voxit).
  * oidc     — Authorization: Bearer <JWT> from any OIDC issuer (edge/2.0+;
    token must carry an email claim).
"""

from __future__ import annotations

from typing import Any

import httpx

from .config import Profile, load_cached_credential, save_cached_credential

API = "/api/v3"


class PolisError(RuntimeError):
    def __init__(self, message: str, response: httpx.Response | None = None):
        super().__init__(message)
        self.response = response


class PolisClient:
    def __init__(self, profile: Profile, *, timeout: float = 30.0):
        self.profile = profile
        # TLS: profiles may set verify=false (dev sandbox) or verify="/path/to/rootCA.pem"
        verify = profile.extra.get("verify", True)
        self._http = httpx.Client(
            base_url=profile.base_url.rstrip("/"),
            timeout=timeout,
            follow_redirects=True,
            verify=verify,
        )
        self._bearer: str | None = None
        self._restore_cached_auth()

    # ------------------------------------------------------------------ auth

    def _restore_cached_auth(self) -> None:
        cred = load_cached_credential(self.profile.name)
        if token := cred.get("bearer"):
            self._bearer = token
        for name, value in cred.get("cookies", {}).items():
            self._http.cookies.set(name, value)

    def _persist_auth(self) -> None:
        save_cached_credential(
            self.profile.name,
            {
                "bearer": self._bearer or "",
                "cookies": dict(self._http.cookies),
            },
        )

    def login_password(self, email: str, password: str) -> None:
        """Legacy session login (stable-branch instances, likely Voxit)."""
        r = self._http.post(f"{API}/auth/login", json={"email": email, "password": password})
        if r.status_code == 404:
            raise PolisError(
                "POST /api/v3/auth/login returned 404 — this instance has the OIDC-only "
                "auth (post-Jul-2025). Use auth='oidc' in the profile.",
                r,
            )
        self._raise_for_status(r, "password login failed")
        self._persist_auth()

    def login_bearer(self, token: str) -> None:
        """Use an externally-obtained OIDC JWT (must carry an email claim)."""
        self._bearer = token
        self._persist_auth()

    def login_oidc_password_grant(
        self,
        email: str,
        password: str,
        *,
        token_url: str | None = None,
        client_id: str | None = None,
        audience: str = "users",
        verify_tls: bool = True,
    ) -> None:
        """OAuth2 resource-owner-password grant against the instance's OIDC issuer.

        Works with the dev OIDC simulator (self-signed TLS: pass verify_tls=False
        or point httpx at the mkcert rootCA) and with Keycloak/Auth0-style issuers
        that allow the password grant for a service account.
        """
        issuer = (token_url or self.profile.oidc_token_url or "").rstrip("/")
        if not issuer:
            raise PolisError("No oidc_token_url configured for this profile.")
        url = issuer if issuer.endswith("/oauth/token") else f"{issuer}/oauth/token"
        r = httpx.post(
            url,
            json={
                "grant_type": "password",
                "username": email,
                "password": password,
                "audience": audience,
                "client_id": client_id or self.profile.oidc_client_id or "dev-client-id",
                "scope": "openid profile email",
            },
            verify=verify_tls,
            timeout=30.0,
        )
        if r.status_code >= 400:
            raise PolisError(f"OIDC token request failed: HTTP {r.status_code} — {r.text[:300]}")
        self._bearer = r.json()["access_token"]
        self._persist_auth()

    # -------------------------------------------------------------- plumbing

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self._bearer:
            headers["Authorization"] = f"Bearer {self._bearer}"
        # legacy XSRF: polis echoes the token in a cookie; mirror it if present
        if xsrf := self._http.cookies.get("XSRF-TOKEN"):
            headers["X-XSRF-TOKEN"] = xsrf
        return headers

    @staticmethod
    def _raise_for_status(r: httpx.Response, context: str) -> None:
        if r.status_code >= 400:
            raise PolisError(f"{context}: HTTP {r.status_code} — {r.text[:300]}", r)

    def _get(self, path: str, **params: Any) -> httpx.Response:
        r = self._http.get(f"{API}{path}", params=params or None, headers=self._headers())
        self._raise_for_status(r, f"GET {path}")
        return r

    def _post(self, path: str, payload: dict | None = None) -> httpx.Response:
        r = self._http.post(f"{API}{path}", json=payload, headers=self._headers())
        self._raise_for_status(r, f"POST {path}")
        return r

    def _put(self, path: str, payload: dict) -> httpx.Response:
        r = self._http.put(f"{API}{path}", json=payload, headers=self._headers())
        self._raise_for_status(r, f"PUT {path}")
        return r

    def call(self, method: str, path: str, *, query: dict | None = None, body: dict | None = None):
        """Generic endpoint call used by the generated full-coverage commands.

        Drops None values; returns parsed JSON when possible, else raw text.
        """
        query = {k: v for k, v in (query or {}).items() if v is not None}
        body = {k: v for k, v in (body or {}).items() if v is not None}
        r = self._http.request(
            method,
            f"{API}{path}" if not path.startswith("/api/") else path,
            params=query or None,
            json=body or None,
            headers=self._headers(),
        )
        self._raise_for_status(r, f"{method} {path}")
        try:
            return r.json()
        except ValueError:
            return {"raw": r.text[:100000], "content_type": r.headers.get("content-type", "")}

    # ---------------------------------------------------------- conversations

    def create_conversation(self, topic: str, description: str = "", **settings: Any) -> dict:
        payload = {"topic": topic, "description": description, **settings}
        return self._post("/conversations", payload).json()

    def update_conversation(self, conversation_id: str, **settings: Any) -> dict:
        payload = {"conversation_id": conversation_id, **settings}
        return self._put("/conversations", payload).json()

    def get_conversation(self, conversation_id: str) -> dict:
        return self._get("/conversations", conversation_id=conversation_id).json()

    def _fire_and_verify_lifecycle(self, path: str, conversation_id: str, want_active: bool) -> None:
        """Upstream bug (stable@adce54b): close/reopen success paths never send an
        HTTP response, so the request hangs. Fire with a short timeout, swallow the
        hang, then verify the state actually changed via GET."""
        try:
            self._http.post(
                f"{API}{path}",
                json={"conversation_id": conversation_id},
                headers=self._headers(),
                timeout=5.0,
            )
        except httpx.TimeoutException:
            pass  # expected on success (see docstring)
        convo = self.get_conversation(conversation_id)
        if bool(convo.get("is_active")) != want_active:
            raise PolisError(f"{path} did not take effect (is_active={convo.get('is_active')})")

    def close_conversation(self, conversation_id: str) -> None:
        self._fire_and_verify_lifecycle("/conversation/close", conversation_id, want_active=False)

    def reopen_conversation(self, conversation_id: str) -> None:
        self._fire_and_verify_lifecycle("/conversation/reopen", conversation_id, want_active=True)

    # ------------------------------------------------------------- statements

    def seed_comment(self, conversation_id: str, text: str) -> dict:
        payload = {"conversation_id": conversation_id, "txt": text, "is_seed": True}
        return self._post("/comments", payload).json()

    def list_comments(self, conversation_id: str, moderation: bool = False) -> list[dict]:
        params: dict[str, Any] = {"conversation_id": conversation_id}
        if moderation:
            params.update({"moderation": "true", "include_unmoderated": "true"})
        return self._get("/comments", **params).json()

    def moderate_comment(self, conversation_id: str, tid: int, accept: bool) -> dict:
        payload = {"conversation_id": conversation_id, "tid": tid, "mod": 1 if accept else -1}
        return self._put("/comments", payload).json()

    # ------------------------------------------------------------------ votes

    def vote(self, conversation_id: str, tid: int, vote: int, pid: str = "mypid") -> dict:
        """vote: -1 agree, 1 disagree, 0 pass (polis wire convention)."""
        payload = {"conversation_id": conversation_id, "tid": tid, "vote": vote, "pid": pid}
        return self._post("/votes", payload).json()

    # ----------------------------------------------------------- math/export

    def math(self, conversation_id: str) -> dict:
        return self._get("/math/pca2", conversation_id=conversation_id).json()

    def create_report(self, conversation_id: str) -> dict:
        return self._post("/reports", {"conversation_id": conversation_id}).json()

    def list_reports(self, conversation_id: str) -> list[dict]:
        return self._get("/reports", conversation_id=conversation_id).json()

    def export_csv(self, report_id: str, kind: str) -> str:
        """kind: comments | votes | participant-votes | comment-groups | summary"""
        r = self._http.get(
            f"{API}/reportExport/{report_id}/{kind}.csv", headers=self._headers()
        )
        self._raise_for_status(r, f"export {kind}")
        return r.text
