# Development Tasks for Claude Code

This file lists the concrete tasks to implement the film recommender.

## Phase 1: Storage & Data

### Task 1.1: Film Storage (src/data/storage.py)
**What:** Implement JSON-based persistence for film analyses

- [ ] `_analysis_to_dict()` - Convert FilmAnalysis dataclass to JSON-serializable dict
- [ ] `_dict_to_analysis()` - Convert dict back to FilmAnalysis dataclass
- [ ] `save_analysis()` - Write analysis to JSON file
- [ ] `load_analysis()` - Read analysis from JSON file
- [ ] `get_all_films()` - Return all analyzed films from the database
- [ ] `exists()` - Check if a film has been analyzed

**Data structure** (films.json):
```json
{
  "films": {
    "Dead Man": {
      "title": "Dead Man",
      "director": "Jim Jarmusch",
      "year": 1995,
      "worldview_core": "...",
      "worldview_elements": [...],
      "technique": [...],
      ...
    }
  }
}
```

**Test**: `python -c "from src.data.storage import FilmStorage; s = FilmStorage(); print(s.db_path)"`

---

### Task 1.2: Film Data Fetcher (src/data/fetcher.py) - OPTIONAL
**What:** Get film metadata from external sources (manual input or scraping)

- [ ] `get_film_metadata()` - Return basic info (director, year, plot)
- [ ] Support multiple sources (user input → manual descriptions)

*Can start with manual descriptions; add IMDb/Wikipedia scraping later*

---

## Phase 2: Analysis

### Task 2.1: Film Analyzer (src/agents/analyzer.py)
**What:** Use Claude API to decompose a film into its worldview/technique/philosophy

- [ ] Initialize Anthropic client in `__init__`
- [ ] `analyze()` - Call Claude to analyze a film
- [ ] `_parse_response()` - Parse Claude's JSON response into FilmAnalysis

**Claude prompt** (roughly):
```
Analyze this film: {title}
{optional_description}

Provide a JSON response with:
- worldview_core: One sentence describing the film's central philosophy
- worldview_elements: List of key philosophical ideas
- technique: List of visual/narrative techniques
- structure: How the film is structured
- tone: Emotional register and formal approach
- philosophy: Extended statement of what the film believes
- rejects: What the film explicitly avoids/rejects
```

**Test**: `python -c "from src.agents.analyzer import FilmAnalyzer; a = FilmAnalyzer(); print(a.analyze('Taxi Driver'))"`

---

## Phase 3: Matching

### Task 3.1: Worldview Categorization (src/agents/matcher.py)
**What:** Map films' philosophies to semantic categories

- [ ] Expand `worldview_categories` dictionary with more categories
- [ ] Implement `_categorize_worldview()` to match philosophy → categories
- [ ] Test categorization against your known taste

**Categories to consider**:
- isolation/alienation
- discipline/code
- decay/inevitability
- corruption/cynicism
- intoxication/seduction
- refusal/acceptance
- system failure
- moral ambiguity

---

### Task 3.2: Film Matcher (src/agents/matcher.py)
**What:** Find films with philosophical/aesthetic alignment

- [ ] Implement `find_aligned()`:
  - Categorize source film worldview
  - For each candidate film:
    - Calculate worldview similarity (category overlap)
    - Calculate tone similarity (emotional register)
    - Calculate rejection alignment
  - Weight: worldview 45%, tone 35%, rejections 20%
  - Return sorted by alignment score
- [ ] Implement `_generate_explanation()` - Prose explaining why films align

**Example output**:
```
Dead Man and Le Samouraï are philosophical cousins.
Both explore [shared_categories] with absolute refusal to compromise.
Both reject: [shared_rejections]

What connects them: [shared tone]
Where they differ: [different genres/settings]
```

**Test**: Create test films with known alignments, verify matching

---

## Phase 4: Recommendations & CLI

### Task 4.1: Recommendation Agent (src/agents/recommender.py)
**What:** Orchestrate the full pipeline

- [ ] `recommend()` - Main method:
  1. Get or analyze the reference film (cache check)
  2. Get all cached films
  3. Find aligned films using matcher
  4. Format and return recommendations
- [ ] `_get_or_analyze_film()` - Load from cache or analyze new
- [ ] `_format_recommendations()` - Pretty output with rankings

**Output format**:
```
═══════════════════════════════════════════════════════════════
RECOMMENDATIONS FOR: Taxi Driver
═══════════════════════════════════════════════════════════════

1. No Country for Old Men (87% alignment)
   Both explore corruption/cynicism with absolute refusal...
   
2. Heat (82% alignment)
   ...
```

---

### Task 4.2: CLI Integration (src/main.py)
**What:** Make the CLI actually work

- [ ] Import RecommendationAgent
- [ ] Replace TODO with actual agent calls
- [ ] Handle film not found errors gracefully
- [ ] Support `quit` command to exit

**Test**: `python -m src.main`

---

## Phase 5: Testing & Polish

### Task 5.1: Basic Tests (tests/)
**What:** Verify core functionality

- [ ] Test storage serialization/deserialization
- [ ] Test analyzer on a real film (costs tokens!)
- [ ] Test matcher on known film pairs
- [ ] Test recommendation pipeline end-to-end

### Task 5.2: Initial Film Database
**What:** Prime the system with films you know

- [ ] Manually analyze 5-10 of your favorite films (or use analyzer + manual review)
- [ ] Store in films.json
- [ ] Test recommendations between them
- [ ] Iterate on categorization if matching seems off

### Task 5.3: Documentation
**What:** Update README with actual examples

- [ ] Document Claude API integration approach
- [ ] Add real example output
- [ ] Document how to add new films

---

## Implementation Notes

### API Costs
- Each `analyze()` call costs tokens (≈500-1000 tokens per film)
- Save analyses in JSON to avoid re-analyzing
- Test locally with cached films before calling API repeatedly

### Matching Tuning
- Start with simple category overlap + tone matching
- If matching seems off, adjust weights or refine categories
- Can later add embeddings if needed

### Storage Design
- Keep films.json human-readable (pretty JSON)
- Version control it (don't put in .gitignore) for sharing taste
- Can later move to SQLite if dataset gets large

---

## Success Criteria

When complete, the system should:

✅ Analyze a film using Claude API
✅ Store analysis in JSON
✅ Find other films with similar worldview
✅ Explain recommendations in plain English
✅ Work via CLI: `python -m src.main`
✅ Re-use cached analyses (no duplicate API calls)
✅ Give recommendations you actually agree with

---

## Priority Order

1. **Storage** (1.1) - Need this before anything else
2. **Analyzer** (2.1) - Core intelligence; test with one film first
3. **Matcher** (3.1, 3.2) - The actual recommendation logic
4. **Recommender + CLI** (4.1, 4.2) - Tie it together
5. **Testing & Polish** (5.x) - Make it production-ready

---

## Questions for You

- How many films to pre-analyze before launching? (5? 10? 50?)
- Should recommendations be limited to analyzed films, or should we analyze on-demand?
- Do you want to add user feedback ("This recommendation was good/bad")?
- Web UI or CLI-only initially?

Assign these tasks to Claude Code via the terminal and watch it build.
