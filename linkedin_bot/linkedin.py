from .config import Config
from .http import post_json


def publish(config: Config, commentary: str) -> str:
    payload = {
        "author": config.linkedin_author_urn,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [],
                         "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    _, headers = post_json(
        "https://api.linkedin.com/rest/posts", payload,
        {"Authorization": f"Bearer {config.linkedin_access_token}",
         "Linkedin-Version": config.linkedin_version,
         "X-Restli-Protocol-Version": "2.0.0"},
    )
    return next((value for key, value in headers.items() if key.lower() == "x-restli-id"),
                "published-id-unavailable")
