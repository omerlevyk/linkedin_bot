from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ApiError(RuntimeError):
    pass


def post_json(url: str, payload: dict, headers: dict[str, str], timeout: int = 60) -> tuple[dict, dict[str, str]]:
    request = Request(url, data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode()
            return (json.loads(body) if body else {}), dict(response.headers.items())
    except HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise ApiError(f"API returned HTTP {exc.code}: {body[:1000]}") from exc
    except URLError as exc:
        raise ApiError(f"API request failed: {exc.reason}") from exc
