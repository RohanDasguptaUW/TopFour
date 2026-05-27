# Phase 1 Development Tasks for Claude Code

Complete task breakdown for building the film recommender with **Top 4 Taste Profiles**.

## Architecture Overview

**User Journey:**
1. User enters 4 favorite films (incrementally)
2. System analyzes each + asks clarifying questions
3. System generates taste profile (poetic + clinical)
4. User asks for recommendations
5. System matches against taste profile, shows connections to Top 4
6. User rates recommendations (structured feedback)
7. System suggests adding highly-aligned films to Top 4
8. User's taste profile evolves

---

## Phase 1A: Foundation (Storage + Data Fetching)

### Task 1.1: Expanded Storage Layer (src/data/storage.py)
**What:** Persistent storage for films, user profiles, and feedback

**Dataclasses to implement:**

```python
@dataclass
class FilmAnalysis:
    title: str
    director: Optional[str]
    year: Optional[int]
    worldview_core: str
    worldview_elements: list[str]
    technique: list[str]
    structure: list[str]
    tone: list[str]
    philosophy: str
    rejects: list[str]

@dataclass
class TasteArchetype:
    poetic: str  # "Elegies for discipline..."
    summary: dict  # {"worldviews": [...], "techniques": [...]}

@dataclass
class UserProfile:
    top_4: list[dict]  # Each with analysis + user_explanation
    taste_archetype: TasteArchetype
    profile_version: int
```

**Methods to implement:**

- [ ] `save_film_analysis(analysis: FilmAnalysis)` - Save to films.json
- [ ] `load_film_analysis(title: str) -> FilmAnalysis` - Load from cache
- [ ] `save_user_profile(profile: UserProfile)` - Save user data
- [ ] `load_user_profile() -> UserProfile` - Load user profile
- [ ] `save_feedback(feedback: dict)` - Store recommendation feedback
- [ ] `load_all_feedback() -> list` - Get all user feedback
- [ ] `film_exists(title: str) -> bool` - Check if analyzed
- [ ] `get_all_analyzed_films() -> list[FilmAnalysis]` - Get database

**Storage structure:**
```
data/
├── films.json          # {film_title: analysis_dict}
├── user_profile.json   # {top_4, archetype, version}
└── feedback.json       # [{recommended, rating, reason, timestamp}]
```

**Test**: 
```bash
python -c "from src.data.storage import FilmStorage; 
s = FilmStorage(); 
p = s.load_user_profile(); 
print(p.taste_archetype if p else 'No profile')"
```

---

### Task 1.2: Film Data Fetcher (src/data/fetcher.py)
**What:** Auto-fetch film metadata from Wikipedia/IMDb

**Methods to implement:**

- [ ] `fetch_film_data(title: str) -> dict` 
  - Returns: {title, director, year, summary, genres, etc.}
  - Try Wikipedia first, fallback to IMDb/manual if needed
- [ ] `_scrape_wikipedia(title: str) -> dict` - Parse Wikipedia
- [ ] `_search_imdb(title: str) -> dict` - IMDb lookup (if API available)
- [ ] Handle not found gracefully (return empty, let user provide description)

**Return format:**
```python
{
    "title": "Dead Man",
    "director": "Jim Jarmusch",
    "year": 1995,
    "summary": "A railroad clerk travels west...",
    "genres": ["Western", "Drama"],
    "runtime": 121
}
```

**Test**: 
```bash
python -c "from src.data.fetcher import FilmFetcher; 
f = FilmFetcher(); 
data = f.fetch_film_data('Taxi Driver'); 
print(data['director'])"
```

---

## Phase 1B: Analysis Pipeline (Analyze + Clarify)

### Task 2.1: Film Analyzer (src/agents/analyzer.py)
**What:** Claude analyzes film to A/B blend level (interpretive + structural)

**Methods to implement:**

- [ ] `analyze(title: str, summary: str) -> FilmAnalysis`
  - Takes film title + plot summary
  - Returns A/B blend analysis (interpretive + structural, not verbose)
  - Use Claude API
  
- [ ] `_build_analysis_prompt(title, summary) -> str`
  - Craft prompt for Claude to analyze film
  - Request JSON output with all FilmAnalysis fields
  
- [ ] `_parse_analysis_response(response: str) -> FilmAnalysis`
  - Parse Claude's JSON into FilmAnalysis dataclass

**Claude prompt level:**
```
Analyze this film deeply but concisely:

Title: {title}
Summary: {summary}

Provide a JSON response with:
{
  "worldview_core": "One sentence central philosophy",
  "worldview_elements": ["Key idea 1", "Key idea 2", ...],
  "technique": ["Visual/narrative technique 1", ...],
  "structure": ["How structured: episodic, cyclical, etc."],
  "tone": ["Emotional register", "Formal approach", ...],
  "philosophy": "Extended statement of what this film believes",
  "rejects": ["What it explicitly avoids: sentimentality, etc."]
}

Be interpretive but precise. Avoid verbose essays.
```

**Test:**
```bash
python -c "from src.agents.analyzer import FilmAnalyzer; 
a = FilmAnalyzer(); 
analysis = a.analyze('Taxi Driver', 'A night cabbie...'); 
print(analysis.philosophy[:50])"
```

---

### Task 2.2: Clarifying Questions Agent (src/agents/analyzer.py - new method)
**What:** Ask open-ended questions to refine film analysis based on user's perspective

**Methods to implement:**

- [ ] `ask_clarifying_question(analysis: FilmAnalysis) -> str`
  - Returns an open-ended question about the film
  - Example: "What about this film resonates most strongly with you?"
  
- [ ] `refine_analysis(analysis: FilmAnalysis, user_explanation: str) -> (FilmAnalysis, str)`
  - Takes original analysis + user's explanation
  - Returns refined analysis + user_explanation to store
  - Use Claude to understand how user's take adds nuance
  - Returns updated analysis + the user's explanation

**Logic:**
```
1. Show user the initial analysis
2. Ask: "What about this resonates?"
3. User explains
4. Claude parses explanation
5. Claude refines the analysis based on user's perspective
6. Store both analysis and user_explanation
```

**Storage note:** Save user's explanation as part of film data:
```python
{
    "title": "Dead Man",
    "analysis": {...},
    "user_explanation": "Death as condition, not climax. Visual discipline reinforces acceptance."
}
```

**Test:**
```bash
python -c "from src.agents.analyzer import FilmAnalyzer; 
a = FilmAnalyzer(); 
refined, explanation = a.refine_analysis(
    analysis, 
    'I love how it treats death as environment'
); 
print(refined.philosophy[:50])"
```

---

## Phase 1C: Taste Profile Generation

### Task 3.1: Taste Profile Generator (src/agents/analyzer.py - new class)
**What:** After all 4 films analyzed, generate unified taste archetype

**Methods to implement:**

```python
class TasteProfileGenerator:
    def generate(self, top_4_analyses: list[FilmAnalysis]) -> TasteArchetype:
        """
        Analyze all 4 films together.
        Return poetic + clinical archetype.
        """
```

- [ ] `_find_common_themes(analyses: list) -> dict`
  - Extract shared worldviews, techniques, tones across all 4
  - Return patterns
  
- [ ] `_generate_poetic_archetype(themes: dict, titles: list) -> str`
  - Use Claude to write evocative taste description
  - Example: "Elegies for discipline: films where formal rigor..."
  - Store this internally
  
- [ ] `_generate_clinical_summary(themes: dict) -> dict`
  - Create structured breakdown for matching + display
  - Return: {"worldviews": [...], "techniques": [...], "tone": [...], "rejects": [...]}
  
- [ ] `generate(top_4_analyses) -> TasteArchetype`
  - Orchestrate: find themes → poetic → clinical
  - Return TasteArchetype with both versions

**Output (stored in user_profile.json):**
```python
TasteArchetype(
    poetic="Elegies for discipline: films where formal rigor and emotional 
            restraint become their own kind of beauty. Characters committed 
            to codes that isolate them. The beauty is in acceptance...",
    summary={
        "worldviews": ["Discipline/code as identity", "Isolation through commitment"],
        "techniques": ["Formal rigor", "Minimal exposition"],
        "tone": ["Deadpan", "Unsentimental"],
        "rejects": ["Sentimentality", "Narrative convenience"]
    }
)
```

**Test:**
```bash
python -c "from src.agents.analyzer import TasteProfileGenerator; 
g = TasteProfileGenerator(); 
archetype = g.generate(analyses_list); 
print(archetype.poetic[:50])"
```

---

## Phase 1D: Matching & Recommendations

### Task 4.1: Film Matcher (src/agents/matcher.py)
**What:** Match films against user's taste profile (not individual film)

**Methods to implement:**

```python
class FilmMatcher:
    def find_aligned_to_taste(
        self, 
        taste_profile: TasteArchetype,
        top_4_films: list[FilmAnalysis],
        candidate_films: list[FilmAnalysis],
        top_n: int = 5
    ) -> list[tuple[FilmAnalysis, float, list[str]]]:
        """
        Find films aligned with taste profile.
        Return list of (film, alignment_score, which_top_4_connect)
        """
```

- [ ] `_categorize_worldview(philosophy: str) -> set`
  - Map film philosophy to worldview categories
  - Categories: discipline/code, isolation, decay, corruption, etc.
  
- [ ] `_calculate_alignment(candidate: FilmAnalysis, taste_summary: dict, top_4: list) -> (float, list)`
  - Score alignment with taste profile
  - Return score (0-1) + which Top 4 films it connects to
  - Weights: worldview 45%, tone 35%, rejections 20%
  - Also note: "Aligns with [Top 4 film] on [shared theme]"
  
- [ ] `find_aligned_to_taste(...)` - Main method
  - Use _categorize_worldview on candidate + taste
  - Calculate alignment
  - Return sorted by score

**Output:**
```python
[
    (
        film_analysis_obj,
        0.89,  # alignment score
        ["Aligns with Dead Man on: Death as condition",
         "Aligns with Taxi Driver on: Moral ambiguity"]
    ),
    ...
]
```

**Test:**
```bash
python -c "from src.agents.matcher import FilmMatcher; 
m = FilmMatcher(); 
matches = m.find_aligned_to_taste(
    taste_archetype, 
    top_4_analyses, 
    all_films
); 
print(matches[0])"
```

---

### Task 4.2: Recommendation Formatter (src/agents/recommender.py)
**What:** Format recommendations with taste-based explanation

**Methods to implement:**

- [ ] `format_recommendations(matches: list, taste_archetype: TasteArchetype) -> str`
  - Takes matched films (from FilmMatcher)
  - Returns formatted recommendations with:
    - Film title + alignment score
    - Which Top 4 films it connects to + why
    - Overall taste theme connection
  
**Output format:**
```
RECOMMENDATIONS BASED ON YOUR TASTE:

Your taste (poetic summary): Elegies for discipline...

1. No Country for Old Men (89% alignment)
   Connects through:
   ✓ Aligns with [Dead Man] on: Death as condition, moral inevitability
   ✓ Aligns with [Taxi Driver] on: Moral ambiguity, no resolution
   ✓ Aligns with [Heat] on: Professional discipline isolates
   ✓ Aligns with [Le Samouraï] on: Formal perfection + acceptance

2. The Conversation (84% alignment)
   ...
```

**Test**: `python -m src.main` and get recommendations

---

## Phase 1E: Feedback & Evolution

### Task 5.1: Feedback Handler (src/agents/recommender.py - new class)
**What:** Capture structured + free-form feedback on recommendations

**Methods to implement:**

```python
class FeedbackHandler:
    def get_feedback(self, film_title: str, alignment_score: float) -> dict:
        """
        Ask user: Do you agree with this recommendation?
        If not, ask why + capture structured + free-form.
        """
```

- [ ] `get_feedback(film_title, score) -> dict`
  - Present recommendation
  - Ask: Do you agree? [Yes/No]
  - If No: Ask "Why?" with structured options
  - Capture free-form explanation
  - Return feedback dict
  
- [ ] Structured feedback options:
  ```
  ☐ Worldview mismatch
  ☐ Tone is too different
  ☐ Techniques don't align
  ☐ Analysis is incomplete
  ☐ Something else: [free-form]
  ```
  
- [ ] `save_feedback(feedback: dict)` - Store to feedback.json
- [ ] `learn_from_feedback(feedback: dict) -> adjustment`
  - Parse feedback
  - Suggest weight adjustment or analysis refinement
  - For now, just store; Phase 2 will use this for retraining

**Storage:**
```python
{
    "recommended_film": "No Country for Old Men",
    "predicted_alignment": 0.89,
    "user_rating": "disagree",
    "feedback_categories": ["worldview_mismatch"],
    "explanation": "Opposite philosophies despite surface alignment",
    "timestamp": "2026-05-28T..."
}
```

---

### Task 5.2: Top 4 Update Suggester (src/agents/recommender.py - new class)
**What:** Suggest adding highly-aligned films to Top 4

**Methods to implement:**

```python
class Top4Suggester:
    def check_for_suggestions(
        self, 
        user_ratings: dict,  # {film: rating}
        taste_profile: TasteArchetype,
        top_4: list[FilmAnalysis]
    ) -> Optional[tuple[str, float]]:
        """
        If user rated a new film 8+/10, check alignment.
        If >85% alignment, suggest adding to Top 4.
        """
```

- [ ] `check_for_suggestions(ratings, taste, top_4) -> Optional[suggestion]`
  - Find films rated 8+ that aren't in Top 4
  - Calculate alignment with taste profile
  - If >85%: Return (film_title, alignment_score) to suggest
  - Otherwise: Return None
  
- [ ] `present_suggestion(film, score) -> str`
  - User-friendly presentation
  - Example: "No Country for Old Men aligns 89% with your taste. Add to Top 4?"
  
- [ ] `update_top_4(new_film, top_4) -> (new_top_4, regenerated_archetype)`
  - Replace one film or add as 5th?
  - Regenerate taste archetype with new Top 4
  - Save to user_profile.json

**Threshold:** >85% alignment for suggestions

**Test**: Rate a new film 9/10, system should suggest if aligned

---

## Phase 1F: CLI Integration

### Task 6.1: Onboarding Loop (src/main.py)
**What:** Interactive Top 4 entry with analysis + clarifying questions

**Flow:**

```
Welcome! Let's build your taste profile.

Enter film 1 of 4: Dead Man
[System fetches data, analyzes]
[Shows analysis]
What about this resonates with you? 
> [User explains]
[System refines analysis]

Enter film 2 of 4: Taxi Driver
...

[After all 4]
Generating your taste archetype...
[Shows poetic + clinical summary]

Your taste profile is ready!
```

- [ ] `onboarding_loop()` - Main entry flow
  - For i in 1..4:
    - Get film title
    - Fetch data
    - Analyze
    - Show analysis
    - Ask clarifying question
    - Get user explanation
    - Refine analysis
    - Save to storage
  - After 4: Generate archetype
  - Save user profile

- [ ] Error handling:
  - Film not found? Ask for summary or try again
  - User wants to skip? Allow it
  - User wants to redo a film? Allow it

---

### Task 6.2: Recommendation Loop (src/main.py)
**What:** Get recommendations, rate them, iterate

**Flow:**

```
What would you like?
1. Get recommendations
2. Update my Top 4
3. Quit

> 1
[Getting recommendations based on your taste...]

[Show recommendations with connections to Top 4]

Do you agree with [Film]? (89% alignment)
[Yes] [No]

If No:
  Why?
  ☐ Worldview mismatch
  ☐ Tone is too different
  [Free-form]
  > [Explanation]
  
  Thanks! System learned from your feedback.

More recommendations? [Yes/No]
```

- [ ] `recommendation_loop()` - Main recommendation flow
  - Get all analyzed films
  - Match against taste profile
  - Present recommendations
  - Collect feedback
  - Store feedback
  
- [ ] Integration with FilmMatcher, FeedbackHandler, Formatter

---

### Task 6.3: Update Loop (src/main.py)
**What:** Check for Top 4 suggestions, let user update manually

**Flow:**

```
You rated "No Country for Old Men" 9/10.
It aligns 89% with your taste.

Add to Top 4? [Yes] [Not yet] [No]

If Yes:
  Regenerating your taste profile with new Top 4...
  [Shows updated archetype]
```

- [ ] Check for high-rated films when rating
- [ ] Present suggestions at >85% threshold
- [ ] Allow manual Top 4 update anytime
- [ ] Regenerate archetype on update

---

### Task 6.4: Main CLI (src/main.py - replace skeleton)
**What:** Tie all loops together

- [ ] Replace TODO skeleton
- [ ] Detect first-time user (no profile) → onboarding_loop()
- [ ] Returning user → menu:
  ```
  1. Get recommendations
  2. Update my Top 4
  3. View my taste profile
  4. Quit
  ```
- [ ] Handle KeyboardInterrupt gracefully
- [ ] Save state frequently

**Test:**
```bash
python -m src.main
# Follow onboarding with your Top 4
# Then get recommendations
# Rate them and see feedback collection
```

---

## Phase 1G: Testing & Validation

### Task 7.1: Storage Tests (tests/test_storage.py)
- [ ] Test saving/loading FilmAnalysis
- [ ] Test saving/loading UserProfile
- [ ] Test feedback persistence
- [ ] Test file encoding/parsing

### Task 7.2: Analysis Tests (tests/test_analyzer.py)
- [ ] Test film analysis returns valid FilmAnalysis
- [ ] Test clarifying question refines analysis
- [ ] Test taste archetype generation on known 4 films

### Task 7.3: Matching Tests (tests/test_matcher.py)
- [ ] Test alignment calculation
- [ ] Test worldview categorization
- [ ] Test that known-good matches score high
- [ ] Test that known-bad matches score low

### Task 7.4: End-to-End Tests (tests/test_e2e.py)
- [ ] Test full onboarding flow
- [ ] Test recommendation generation
- [ ] Test feedback → learning loop

---

## Implementation Priority

**Must have (Phase 1A):**
1. Task 1.1 - Storage (blocks everything)
2. Task 1.2 - Film Fetcher (needed for analysis)

**Core intelligence (Phase 1B-C):**
3. Task 2.1 - Film Analyzer
4. Task 2.2 - Clarifying Questions
5. Task 3.1 - Taste Profile Generator

**Matching & feedback (Phase 1D-E):**
6. Task 4.1 - Film Matcher
7. Task 4.2 - Recommendation Formatter
8. Task 5.1 - Feedback Handler
9. Task 5.2 - Top 4 Suggester

**Integration (Phase 1F):**
10. Task 6.1-6.4 - CLI loops
11. Task 7.x - Testing

---

## Success Criteria

By end of Phase 1:

✅ User can enter Top 4 films incrementally
✅ System analyzes each film (A/B blend)
✅ System asks clarifying questions (open-ended)
✅ System generates taste archetype (poetic + clinical)
✅ User can ask for recommendations
✅ System matches against taste profile (not individual films)
✅ Recommendations show which Top 4 films they connect to
✅ User can rate recommendations (structured + free-form feedback)
✅ System suggests adding high-aligned films to Top 4 (>85% threshold)
✅ Everything persists (films.json, user_profile.json, feedback.json)
✅ CLI is fully functional and user-friendly

---

## Key Design Decisions (Locked In)

✅ **Analysis level**: A/B blend (interpretive + structural, not verbose essays)
✅ **Clarifying questions**: Open-ended ("What resonates?")
✅ **Taste archetype**: Hybrid (poetic internally, clinical for display)
✅ **Recommendations**: Taste-based (show Top 4 connections)
✅ **Feedback**: Structured + free-form (categories + explanation)
✅ **Top 4 updates**: Suggested at >85% threshold + manual anytime
✅ **Regeneration**: Full archetype regenerate on Top 4 update
✅ **Privacy**: All data private (Phase 2 will add sharing)

---

## API Cost Management

- Each `analyze()` call: ~500-1000 tokens
- Each `refine_analysis()` call: ~300-500 tokens
- Each `generate_archetype()` call: ~1000 tokens
- Total for 4-film onboarding: ~4000-8000 tokens
- **Cache aggressively**: Don't re-analyze, ever

**Strategy:**
- Analyze + clarify in one pass (don't re-analyze)
- Store everything
- Use cached data for matching (no re-computation)

---

## Questions for Rohan (To Ask When Building)

- Film fetcher: Priority on Wikipedia vs. IMDb?
- Should onboarding be resumable? (Start Top 4, quit, come back later?)
- Should users be able to edit their explanations after entering?
- Feedback: Store only disagree, or all ratings?

Let Claude Code ask these when it makes sense.
