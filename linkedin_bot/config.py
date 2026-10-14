from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_TOPICS = (
    "networking", "Kubernetes", "OpenShift", "cloud architecture", "Linux",
    "servers", "Azure", "AWS", "Terraform", "Crossplane", "Ansible",
    "infrastructure as code", "Go", "Python", "Git",
    "DevOps career development", "MLOps", "observability", "CI/CD",
    "containers", "security", "reliability engineering",
)


def _boolean(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be true or false")


@dataclass(frozen=True)
class Config:
    openai_api_key: str
    openai_model: str
    linkedin_access_token: str
    linkedin_author_urn: str
    linkedin_version: str
    dry_run: bool
    language: str
    tone: str
    max_chars: int
    state_path: str
    topics: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "Config":
        dry_run = _boolean("DRY_RUN", True)
        topic_value = os.getenv("TOPICS", "")
        topics = tuple(x.strip() for x in topic_value.split(",") if x.strip()) or DEFAULT_TOPICS
        config = cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-5-mini").strip(),
            linkedin_access_token=os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip(),
            linkedin_author_urn=os.getenv("LINKEDIN_AUTHOR_URN", "").strip(),
            linkedin_version=os.getenv("LINKEDIN_VERSION", "202609").strip(),
            dry_run=dry_run,
            language=os.getenv("POST_LANGUAGE", "English").strip(),
            tone=os.getenv("POST_TONE", "practical, friendly, concise, and technically accurate").strip(),
            max_chars=int(os.getenv("POST_MAX_CHARS", "2600")),
            state_path=os.getenv("STATE_PATH", "/data/history.json").strip(),
            topics=topics,
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not self.dry_run and not self.linkedin_access_token:
            raise ValueError("LINKEDIN_ACCESS_TOKEN is required when DRY_RUN=false")
        if not self.dry_run and not self.linkedin_author_urn.startswith("urn:li:person:"):
            raise ValueError("LINKEDIN_AUTHOR_URN must start with urn:li:person:")
        if len(self.linkedin_version) != 6 or not self.linkedin_version.isdigit():
            raise ValueError("LINKEDIN_VERSION must use YYYYMM format")
        if not 200 <= self.max_chars <= 2900:
            raise ValueError("POST_MAX_CHARS must be between 200 and 2900")
