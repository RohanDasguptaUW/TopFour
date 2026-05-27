"""Configuration and utilities."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / "cache"

# Ensure dirs exist
CACHE_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# API Keys (validated lazily — only fail when actually used by agents)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# App config
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
FILMS_DB = DATA_DIR / "films.json"
USER_PROFILE_DB = DATA_DIR / "user_profile.json"
FEEDBACK_DB = DATA_DIR / "feedback.json"
