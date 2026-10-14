from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class History:
    def __init__(self, path: str, limit: int = 30):
        self.path = Path(path)
        self.limit = limit

    def load(self) -> list[dict[str, str]]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Could not read history at {self.path}: {exc}") from exc

    @staticmethod
    def digest(post: str) -> str:
        normalized = " ".join(post.lower().split())
        return hashlib.sha256(normalized.encode()).hexdigest()

    def contains(self, post: str) -> bool:
        digest = self.digest(post)
        return any(item.get("sha256") == digest for item in self.load())

    def add(self, post: str, post_id: str) -> None:
        entries = self.load()
        entries.append({
            "created_at": datetime.now(timezone.utc).isoformat(),
            "sha256": self.digest(post),
            "post_id": post_id,
            "preview": " ".join(post.split())[:180],
        })
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(entries[-self.limit:], indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.path)
