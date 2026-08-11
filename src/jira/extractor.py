"""Extração de issues do Jira Cloud e conversão para o schema comum (Artefato).

Endpoint: GET /rest/api/3/search/jql — Jira Cloud REST API v3.
Fonte: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-get
Autenticação: Basic Auth com e-mail + API token.
Fonte: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
"""

from __future__ import annotations

import os

import requests
from dotenv import load_dotenv

from src.common.schema import Artefato, Subtarefa
from src.jira.adf_parser import (
    adf_to_markdown,
    extract_bullet_items_after_label,
    strip_section_after_label,
)

load_dotenv()

CRITERIOS_ACEITACAO_LABEL = "Critérios de aceitação"


def _get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente {name} não definida. Veja .env.example.")
    return value


def fetch_issues(jql: str | None = None, max_results: int = 100) -> list[dict]:
    """Busca todas as issues via GET /rest/api/3/search/jql, paginando com
    `nextPageToken` até `isLast` vir `true` (paginação por token, não por
    `startAt` — é o modelo do endpoint /search/jql, que substituiu o antigo
    /search baseado em offset)."""
    domain = _get_env("JIRA_DOMAIN")
    email = _get_env("JIRA_EMAIL")
    api_token = _get_env("JIRA_API_TOKEN")

    url = f"https://{domain}/rest/api/3/search/jql"
    params: dict[str, str | int] = {"jql": jql or "", "maxResults": max_results}
    issues: list[dict] = []

    while True:
        response = requests.get(url, params=params, auth=(email, api_token), timeout=30)
        response.raise_for_status()
        payload = response.json()
        issues.extend(payload.get("issues", []))
        if payload.get("isLast", True):
            break
        params["nextPageToken"] = payload["nextPageToken"]

    return issues


def _parse_subtarefas(fields: dict) -> list[Subtarefa]:
    return [
        Subtarefa(
            chave=subtask["key"],
            titulo=subtask["fields"]["summary"],
            status=subtask["fields"]["status"]["name"],
        )
        for subtask in fields.get("subtasks", []) or []
    ]


def parse_issue(issue: dict) -> Artefato:
    """Converte uma issue crua (JSON da API) em `Artefato`."""
    fields = issue["fields"]
    descricao_adf = fields.get("description")
    priority = fields.get("priority")
    assignee = fields.get("assignee")
    descricao_sem_criterios_adf = strip_section_after_label(
        descricao_adf, CRITERIOS_ACEITACAO_LABEL
    )

    return Artefato(
        chave=issue["key"],
        titulo=fields["summary"],
        tipo=fields["issuetype"]["name"],
        status=fields["status"]["name"],
        descricao=adf_to_markdown(descricao_sem_criterios_adf),
        prioridade=priority.get("name") if priority else None,
        responsavel=assignee.get("displayName") if assignee else None,
        labels=fields.get("labels", []) or [],
        subtarefas=_parse_subtarefas(fields),
        criterios_aceitacao=extract_bullet_items_after_label(
            descricao_adf, CRITERIOS_ACEITACAO_LABEL
        ),
    )


def parse_issues(issues: list[dict]) -> list[Artefato]:
    return [parse_issue(issue) for issue in issues]
