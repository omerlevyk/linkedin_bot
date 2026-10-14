import json
import os
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

from linkedin_bot.config import Config
from linkedin_bot.generator import _extract_text, choose_subject
from linkedin_bot.history import History


class ConfigTests(unittest.TestCase):
    def test_dry_run_needs_only_openai_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test", "DRY_RUN": "true"}, clear=True):
            config = Config.from_env()
        self.assertTrue(config.dry_run)
        self.assertGreater(len(config.topics), 10)

    def test_live_mode_requires_linkedin_credentials(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test", "DRY_RUN": "false"}, clear=True):
            with self.assertRaisesRegex(ValueError, "LINKEDIN_ACCESS_TOKEN"):
                Config.from_env()


class GeneratorTests(unittest.TestCase):
    def test_extracts_response_text(self):
        response = {"output": [{"type": "message", "content": [
            {"type": "output_text", "text": "Hello engineers"}
        ]}]}
        self.assertEqual(_extract_text(response), "Hello engineers")

    def test_subject_selection_is_stable(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test"}, clear=True):
            config = Config.from_env()
        day = date(2026, 10, 14)
        self.assertEqual(choose_subject(config, day), choose_subject(config, day))


class HistoryTests(unittest.TestCase):
    def test_persists_and_detects_posts(self):
        with tempfile.TemporaryDirectory() as directory:
            history = History(os.path.join(directory, "history.json"))
            self.assertFalse(history.contains("A post"))
            history.add("A post", "urn:li:share:1")
            self.assertTrue(history.contains("  a   POST "))
            data = json.loads(history.path.read_text())
            self.assertEqual(data[0]["post_id"], "urn:li:share:1")
