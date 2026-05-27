"""
Film Storage
============

Persistent storage for film analyses, user profiles, and feedback.
Three JSON files: films.json, user_profile.json, feedback.json.
"""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from src.agents.analyzer import FilmAnalysis
from src.utils.config import FILMS_DB, USER_PROFILE_DB, FEEDBACK_DB


@dataclass
class TasteArchetype:
    poetic: str  # "Elegies for discipline..."
    summary: dict  # {"worldviews": [...], "techniques": [...]}


@dataclass
class UserProfile:
    top_4: list  # Each entry: {"analysis": {...}, "user_explanation": str}
    taste_archetype: TasteArchetype
    profile_version: int


class FilmStorage:
    """Manages persistent storage of film analyses, user profile, and feedback."""

    def __init__(
        self,
        db_path: Optional[Path] = None,
        profile_path: Optional[Path] = None,
        feedback_path: Optional[Path] = None,
    ):
        self.db_path = db_path or FILMS_DB
        self.profile_path = profile_path or USER_PROFILE_DB
        self.feedback_path = feedback_path or FEEDBACK_DB

        for path in (self.db_path, self.profile_path, self.feedback_path):
            path.parent.mkdir(parents=True, exist_ok=True)

        self._ensure_files_exist()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_files_exist(self):
        if not self.db_path.exists():
            self.db_path.write_text(json.dumps({}, indent=2))
        if not self.profile_path.exists():
            self.profile_path.write_text(json.dumps({}, indent=2))
        if not self.feedback_path.exists():
            self.feedback_path.write_text(json.dumps([], indent=2))

    def _load_json(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_json(self, path: Path, data) -> None:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _analysis_to_dict(self, analysis: FilmAnalysis) -> dict:
        return asdict(analysis)

    def _dict_to_analysis(self, data: dict) -> FilmAnalysis:
        return FilmAnalysis(
            title=data["title"],
            director=data.get("director"),
            year=data.get("year"),
            worldview_core=data["worldview_core"],
            worldview_elements=data["worldview_elements"],
            technique=data["technique"],
            structure=data["structure"],
            tone=data["tone"],
            philosophy=data["philosophy"],
            rejects=data["rejects"],
        )

    # ------------------------------------------------------------------
    # Film analysis
    # ------------------------------------------------------------------

    def save_film_analysis(self, analysis: FilmAnalysis) -> None:
        """Save a FilmAnalysis to films.json, keyed by title."""
        db = self._load_json(self.db_path)
        db[analysis.title] = self._analysis_to_dict(analysis)
        self._save_json(self.db_path, db)

    def load_film_analysis(self, title: str) -> Optional[FilmAnalysis]:
        """Load a FilmAnalysis by title; returns None if not found."""
        db = self._load_json(self.db_path)
        data = db.get(title)
        if data is None:
            return None
        return self._dict_to_analysis(data)

    def film_exists(self, title: str) -> bool:
        """Return True if a film analysis is already cached."""
        db = self._load_json(self.db_path)
        return title in db

    def get_all_analyzed_films(self) -> list:
        """Return all stored FilmAnalysis objects."""
        db = self._load_json(self.db_path)
        return [self._dict_to_analysis(v) for v in db.values()]

    # ------------------------------------------------------------------
    # User profile
    # ------------------------------------------------------------------

    def save_user_profile(self, profile: UserProfile) -> None:
        """Persist the user profile to user_profile.json."""
        data = {
            "top_4": profile.top_4,
            "taste_archetype": {
                "poetic": profile.taste_archetype.poetic,
                "summary": profile.taste_archetype.summary,
            },
            "profile_version": profile.profile_version,
        }
        self._save_json(self.profile_path, data)

    def load_user_profile(self) -> Optional[UserProfile]:
        """Load the user profile; returns None if no profile saved yet."""
        data = self._load_json(self.profile_path)
        if not data:
            return None
        archetype_data = data["taste_archetype"]
        return UserProfile(
            top_4=data["top_4"],
            taste_archetype=TasteArchetype(
                poetic=archetype_data["poetic"],
                summary=archetype_data["summary"],
            ),
            profile_version=data["profile_version"],
        )

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------

    def save_feedback(self, feedback: dict) -> None:
        """Append a feedback entry to feedback.json."""
        entries = self._load_json(self.feedback_path)
        entries.append(feedback)
        self._save_json(self.feedback_path, entries)

    def load_all_feedback(self) -> list:
        """Return all stored feedback entries."""
        return self._load_json(self.feedback_path)
