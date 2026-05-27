# Film Worldview Recommender

A film recommendation engine that matches based on **philosophical alignment and formal discipline**, not genre or cast.

Instead of "you watched *Taxi Driver*, so you'll like *Joker*" (both have isolated protagonists), this agent asks: *Does the film share the same worldview, aesthetic rigor, and rejection of sentimentality?*

## Vision

Most recommenders are shallow: they match on plot, genre, cast, or surface-level similarity. This one is **critical and analytical**:

- **Analyzes** a film's core worldview, technique, and philosophical stance
- **Matches** on thematic/structural alignment, not superficial features
- **Explains** why recommendations work, not just listing them
- **Learns** as you use it (every film analyzed improves future matching)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ User Input: "Recommend based on Dead Man"              │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ Film Data Fetcher                                       │
│ (IMDb, Wikipedia, user input)                          │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ Analysis Agent (Claude API)                            │
│ Decomposes: worldview, technique, tone, philosophy     │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ Analysis Cache (JSON/SQLite)                           │
│ Stores films + their decompositions                    │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ Matching Agent                                          │
│ Semantic similarity + rejection alignment              │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│ Recommendation Agent                                    │
│ Ranks + explains recommendations                       │
└─────────────────────────────────────────────────────────┘
```

## Project Structure

```
film-recommender/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analyzer.py         # Film analysis (Claude API)
│   │   ├── matcher.py          # Find aligned films
│   │   └── recommender.py      # Generate recommendations
│   ├── data/
│   │   ├── __init__.py
│   │   ├── fetcher.py          # Get film data (IMDb, Wikipedia, etc.)
│   │   ├── storage.py          # Persistent cache (films.json)
│   │   └── films.json          # Local film database
│   ├── utils/
│   │   ├── __init__.py
│   │   └── config.py           # Config + API keys
│   └── lib/
│       ├── __init__.py
│       └── semantic.py         # Semantic matching logic
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   └── test_matcher.py
└── .claude-code.json           # Claude Code config
```

## Key Design Decisions

### 1. **Persistent Film Cache**
Every film analyzed gets stored locally (JSON). This means:
- Faster subsequent queries
- System learns and improves over time
- Can see your recommendation history

### 2. **Claude API for Analysis**
Instead of hardcoded film descriptions, use Claude to analyze:
- What makes a film's worldview unique?
- What techniques does it use?
- What does it explicitly reject?

This scales to any film, not just your personal taste.

### 3. **Semantic Matching**
Match films based on:
- **Worldview categories** (isolation/alienation, discipline/code, decay, corruption, etc.)
- **Tone alignment** (formal distance, emotional register)
- **Rejection overlap** (both reject sentimentality? easy answers? character growth?)

### 4. **Interactive CLI**
Simple interface:
```bash
python -m src.main
> Recommend based on: Taxi Driver
> Top N recommendations: 3
```

## TODO

- [ ] Basic CLI structure
- [ ] Film data fetcher (start with manual descriptions)
- [ ] Analysis agent (Claude API integration)
- [ ] Matching algorithm (semantic + rejection alignment)
- [ ] Persistent storage (JSON-based cache)
- [ ] Recommendation generation + explanation
- [ ] Tests
- [ ] Documentation

## Setup

```bash
# Clone
git clone <repo>
cd film-recommender

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your ANTHROPIC_API_KEY

# Run
python -m src.main
```

## Example Usage

```
> Recommend based on: Dead Man
> Top N recommendations: 3

[Analyzing Dead Man...]
Philosophy: Life is about witnessing and enduring, not achieving.
Technique: Desaturated visuals, static composition, spare dialogue
Tone: Deadpan, elegiac, unsentimental

[Finding aligned films...]

1. Le Samouraï (87% alignment)
   Both refuse sentimentality. Both use long stretches of visual observation.
   Both treat death not as climax but as the underlying condition.
   
2. No Country for Old Men (78% alignment)
   Both present a world where the system is rigged and moral clarity is impossible.
   Both end with refusal of narrative satisfaction.
   
3. Chinatown (72% alignment)
   Both explore how corruption is foundational, not exceptional.
   Both feature protagonists who fail despite competence.
```

## Questions to Answer (via Claude Code)

1. **Data source**: Manual descriptions, IMDb scraping, or pure Claude-based analysis?
2. **Matching sophistication**: Simple semantic categories or embeddings?
3. **Scope**: Start with your taste, expand to user-submitted films?
4. **Validation**: How do you test if recommendations are good?

## Notes for Development

- Use Claude Code for iterative development
- Keep matching logic interpretable (explainable recommendations > black-box accuracy)
- Prioritize depth over breadth (better analysis of 50 films > shallow analysis of 10k)
- Test against your own judgment first

---

**This is a Claude Code project.** Use it to iterate, refactor, and build out the components.
