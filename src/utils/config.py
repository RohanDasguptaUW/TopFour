"""Configuration and utilities."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_ROOT = Path(__file__).parent.parent
DATA_DIR = SRC_ROOT / "data"
CACHE_DIR = PROJECT_ROOT / "cache"

# Ensure cache dir exists
CACHE_DIR.mkdir(exist_ok=True)

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in .env")

# App config
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
FILMS_DB = SRC_ROOT / "data" / "films.json"
