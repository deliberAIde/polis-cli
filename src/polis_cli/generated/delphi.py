"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='delphi endpoints (6)', no_args_is_help=True)


@app.command("list", help="[experimental] Returns LLM-generated topic names for a conversation from DynamoDB table Delphi_CommentClustersLLMTopicNames, grouped into 'runs' keyed by model name + created date; also probes Delphi_")
def get_delphi_list(
    report_id: str = typer.Option(..., "--report-id", help="raw req.query string, validated in handler (400 if missing); resolved to zid via getZidFro"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/delphi", query={"report_id": report_id}, body={})
    emit(result)


@app.command("create-batchreports", help="[experimental] Enqueues a CREATE_NARRATIVE_BATCH job in the DynamoDB Delphi_JobQueue to generate batch narrative reports via the Anthropic batch API; job_id is 'batch_report_<report_id>_<ts>_<rand>'.")
def create_delphi_create_batchreports(
    report_id: str = typer.Option(..., "--report-id", help="string (error JSON if missing)"),
    model: Optional[str] = typer.Option(None, "--model", help="string; defaults to ANTHROPIC_MODEL env var — error if neither is set"),
    max_batch_size: Optional[str] = typer.Option(None, "--max-batch-size", help="number (default 20)"),
    no_cache: Optional[str] = typer.Option(None, "--no-cache", help="boolean (default false)"),
    include_moderation: Optional[str] = typer.Option(None, "--include-moderation", help="boolean"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/delphi/batchReports", query={}, body={"report_id": report_id, "model": model, "max_batch_size": max_batch_size, "no_cache": no_cache, "include_moderation": include_moderation})
    emit(result)


@app.command("create-jobs", help='[experimental] Creates a Delphi ML job (UMAP/topic-modeling/narrative pipeline) by writing a PENDING item into the DynamoDB Delphi_JobQueue table (uuid job_id, 4h timeout, max 3 retries). Per source c')
def create_delphi_create_jobs(
    report_id: Optional[str] = typer.Option(None, "--report-id", help="string; one of report_id or conversation_id is required (400 if both missing)"),
    conversation_id: Optional[str] = typer.Option(None, "--conversation-id", help="string; one of report_id or conversation_id is required"),
    job_type: Optional[str] = typer.Option(None, "--job-type", help="string (default 'FULL_PIPELINE')"),
    priority: Optional[str] = typer.Option(None, "--priority", help="int (default 50)"),
    include_moderation: Optional[str] = typer.Option(None, "--include-moderation", help="Ignore comments with failing moderation score"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/delphi/jobs", query={}, body={"report_id": report_id, "conversation_id": conversation_id, "job_type": job_type, "priority": priority, "include_moderation": include_moderation})
    emit(result)


@app.command("get-logs", help="[internal] Fetches CloudWatch log events for a Delphi job (filter pattern '[DELPHI JOB <first 8 chars of job_id>') restricted to the last 3 hours, from the log group in Config.awsLogGroupName.")
def get_delphi_get_logs(
    job_id: str = typer.Option(..., "--job-id", help="raw req.query string — NOT validated: missing job_id causes a TypeError (job_id.slice) and"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/delphi/logs", query={"job_id": job_id}, body={})
    emit(result)


@app.command("get-reports", help='[experimental] Retrieves LLM-generated narrative report sections for a report from the DynamoDB Delphi_NarrativeReports table (GSI ReportIdTimestampIndex), optionally filtered by section, topic_key, o')
def get_delphi_get_reports(
    report_id: str = typer.Option(..., "--report-id", help="raw req.query string; validated to resolve to a zid, then used as the DynamoDB GSI partiti"),
    section: Optional[str] = typer.Option(None, "--section", help="Filter to a specific narrative section"),
    topic_key: Optional[str] = typer.Option(None, "--topic-key", help="Filter to a specific topic's report"),
    job_id: Optional[str] = typer.Option(None, "--job-id", help="Fetch sections from a specific Delphi job run"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/delphi/reports", query={"report_id": report_id, "section": section, "topic_key": topic_key, "job_id": job_id}, body={})
    emit(result)


@app.command("get-visualizations", help='[experimental] Retrieves Delphi-generated visualization data (topic/cluster visualizations produced by the ML pipeline) for a report from DynamoDB.')
def get_delphi_get_visualizations(
    report_id: str = typer.Option(..., "--report-id", help="raw req.query string"),
    job_id: Optional[str] = typer.Option(None, "--job-id", help="Specific job run's visualization data"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/delphi/visualizations", query={"report_id": report_id, "job_id": job_id}, body={})
    emit(result)

