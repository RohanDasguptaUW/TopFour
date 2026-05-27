# Quick Start: Developing with Claude Code

## Setup

1. **Clone to your local machine** (or navigate to the project)
```bash
cd film-recommender
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API key**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

5. **Verify setup**
```bash
python -m src.main
```

You should see a message about skeleton code that needs implementation.

---

## Using Claude Code

### Start Claude Code in the project
```bash
cd film-recommender
claude-code .
```

This starts Claude Code in your terminal with access to the entire project.

### Example: Assign Task 1.1 (Storage)

Tell Claude Code:
```
Implement src/data/storage.py to handle JSON persistence.

Read TASKS.md under "Task 1.1: Film Storage" for full requirements.

Implement these methods:
- _analysis_to_dict()
- _dict_to_analysis()
- save_analysis()
- load_analysis()
- get_all_films()
- exists()

Use the FilmAnalysis dataclass structure. Keep films.json human-readable.
```

Claude Code will:
- Read the existing skeleton
- Implement the methods
- Write the code
- You approve/iterate

### Iterate as Claude Code works

After Claude Code implements something:
```bash
# Test it
python -c "from src.data.storage import FilmStorage; s = FilmStorage(); print(s.db_path)"

# See what got created
cat src/data/films.json
```

If you want changes:
```
The implementation is mostly good, but:
- films.json should be created in the src/data directory, not project root
- Fix the path in the _ensure_db_exists method
```

Claude Code will adjust.

---

## Development Workflow

1. **Pick a task from TASKS.md**
2. **Tell Claude Code the task** (copy-paste the requirement)
3. **Claude Code implements it**
4. **You test locally** (`python -m src.main`, run tests)
5. **Iterate** if needed
6. **Commit to git** when working

Example flow:
```bash
# Test what Claude Code built
python -c "from src.agents.analyzer import FilmAnalyzer; a = FilmAnalyzer(); print('Analyzer loaded')"

# Run the CLI
python -m src.main

# If something's wrong, tell Claude Code
# If it's good, commit
git add -A
git commit -m "Implement storage layer"
```

---

## Key Files to Know

- `README.md` - Project overview and architecture
- `TASKS.md` - Concrete implementation tasks (share with Claude Code)
- `src/main.py` - CLI entry point
- `src/agents/` - The three agents (analyzer, matcher, recommender)
- `src/data/` - Storage and data fetching
- `src/utils/config.py` - Configuration and API keys

---

## Testing Your Work

### Test storage
```python
from src.data.storage import FilmStorage
from src.agents.analyzer import FilmAnalysis

storage = FilmStorage()

# Create a test analysis
test_film = FilmAnalysis(
    title="Test Film",
    director="Test Director",
    year=2024,
    worldview_core="Test worldview",
    worldview_elements=["test"],
    technique=["test"],
    structure=["test"],
    tone=["test"],
    philosophy="Test philosophy",
    rejects=["test"]
)

# Save and load
storage.save_analysis(test_film)
loaded = storage.load_analysis("Test Film")
print(loaded)
```

### Test analyzer (costs tokens!)
```python
from src.agents.analyzer import FilmAnalyzer

analyzer = FilmAnalyzer()
analysis = analyzer.analyze("Taxi Driver")
print(analysis)
```

### Test the full pipeline
```bash
python -m src.main
# > Recommend based on: Taxi Driver
# > Top N recommendations: 3
```

---

## Git Workflow

After each working feature:
```bash
git add -A
git commit -m "Implement [feature]: [brief description]"
git push
```

Example commits:
```
git commit -m "Implement storage: JSON serialization for FilmAnalysis"
git commit -m "Implement analyzer: Claude API integration for film analysis"
git commit -m "Implement matcher: worldview categorization and alignment scoring"
git commit -m "Implement recommender: orchestrate full pipeline"
git commit -m "Complete CLI: integrate all agents into main.py"
```

---

## Tips

- **Cost management**: Cache film analyses! Don't re-analyze.
- **Debugging**: Set `DEBUG=true` in `.env` to get full stack traces
- **Testing**: Use Claude Code to write tests as you go
- **Documentation**: Claude Code can help write docstrings and comments
- **Refactoring**: Once Phase 1-2 work, Claude Code can optimize and reorganize

---

## When You're Done

You'll have a working recommender that:
- Analyzes films using Claude API
- Matches based on worldview + technique
- Explains recommendations in plain English
- Caches everything for fast re-use

Then you can:
- Add more films to the database
- Tune the matching algorithm
- Build a web UI
- Share your taste with others
- Use it to actually find movies to watch

Good luck. Use Claude Code aggressively—that's what it's for.
