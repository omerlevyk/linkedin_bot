import logging

from .config import Config
from .generator import generate
from .history import History
from .linkedin import publish


LOGGER = logging.getLogger("linkedin_bot")


def run() -> None:
    config = Config.from_env()
    history = History(config.state_path)
    previews = [x.get("preview", "") for x in history.load() if x.get("preview")]
    post = generate(config, previews)
    if history.contains(post):
        raise RuntimeError("Generated post matches a previous post; refusing to publish")
    if config.dry_run:
        print("--- DRY RUN: generated LinkedIn post ---")
        print(post)
        print("--- end ---")
        return
    post_id = publish(config, post)
    history.add(post, post_id)
    LOGGER.info("Published LinkedIn post: %s", post_id)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        run()
        return 0
    except Exception as exc:
        LOGGER.error("linkedin_bot failed: %s", exc)
        return 1
