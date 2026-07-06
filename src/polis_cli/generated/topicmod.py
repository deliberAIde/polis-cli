"""AUTO-GENERATED from api/endpoints.json — do not edit by hand.

Regenerate: python scripts/generate_commands.py
Source: compdemocracy/polis stable@adce54b (2026-07-05)
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from ..runtime import get_client, emit

app = typer.Typer(help='topicmod endpoints (6)', no_args_is_help=True)


@app.command("get-topicmod-hierarchy", help='[experimental] Returns the multi-layer topic/cluster hierarchy for a conversation, structured from Delphi cluster records across clustering layers.')
def get_topicmod_get_topicmod_hierarchy(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/topicMod/hierarchy", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("create-topicmod-moderate", help='[experimental] Applies a moderation action (accept/reject/meta) to a whole topic and/or individual comments, upserting DynamoDB Delphi_TopicModerationStatus / comment records.')
def create_topicmod_create_topicmod_moderate(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    action: str = typer.Option(..., "--action", help="string enum: 'accept' | 'reject' | 'meta'"),
    moderator: str = typer.Option(..., "--moderator", help="string (free-text moderator name)"),
    topic_key: Optional[str] = typer.Option(None, "--topic-key", help="If given, moderates the entire topic"),
    comment_ids: Optional[str] = typer.Option(None, "--comment-ids", help="Individual comment ids to moderate instead of/in addition to a whole topic"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("POST", "/api/v3/topicMod/moderate", query={}, body={"conversation_id": conversation_id, "action": action, "moderator": moderator, "topic_key": topic_key, "comment_ids": comment_ids})
    emit(result)


@app.command("get-topicmod-proximity", help="[experimental] Returns comment proximity data — UMAP coordinate points for the conversation's comments — for rendering the topic-moderation proximity view.")
def get_topicmod_get_topicmod_proximity(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    layer_id: Optional[str] = typer.Option(None, "--layer-id", help="Restrict UMAP points to one clustering layer"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/topicMod/proximity", query={"conversation_id": conversation_id, "layer_id": layer_id}, body={})
    emit(result)


@app.command("get-topicmod-stats", help='[experimental] Returns aggregate topic-moderation statistics for a conversation: counts of total topics and pending/accepted/rejected/meta statuses.')
def get_topicmod_get_topicmod_stats(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/topicMod/stats", query={"conversation_id": conversation_id}, body={})
    emit(result)


@app.command("get-topicmod-topics", help='[experimental] Lists Delphi-discovered topics for a conversation grouped by clustering layer, each annotated with its moderation status (from Delphi_TopicModerationStatus).')
def get_topicmod_get_topicmod_topics(
    conversation_id: str = typer.Option(..., "--conversation-id", help="getConversationIdFetchZid (zid)"),
    job_id: Optional[str] = typer.Option(None, "--job-id", help="Restrict to topics from a specific Delphi job"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", "/api/v3/topicMod/topics", query={"conversation_id": conversation_id, "job_id": job_id}, body={})
    emit(result)


@app.command("get-topicmod-topics-comments", help='[experimental] List comments assigned to a Delphi ML topic cluster (from DynamoDB Delphi_CommentClusters), with UMAP coordinates and per-comment moderation status — used by topic-based moderation UI.')
def get_topicmod_get_topicmod_topics_comments(
    topicKey: str = typer.Argument(..., help="path param topicKey"),
    conversation_id: str = typer.Option(..., "--conversation-id", help="conversation whose Delphi comment clusters to query"),
    profile: str = typer.Option("local", "--profile", "-p"),
):
    client = get_client(profile)
    result = client.call("GET", f"/api/v3/topicMod/topics/{topicKey}/comments", query={"conversation_id": conversation_id}, body={})
    emit(result)

