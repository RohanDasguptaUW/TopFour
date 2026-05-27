# TopFour

A film recommendation engine that matches based on **worldview, technique, and aesthetic philosophy** — not genre, cast, or plot similarity.

## The Problem

Most film recommenders are shallow. They match on surface-level features: "You watched a thriller, so here's another thriller." "You liked this actor, so here's their other films."

But meaningful recommendations require deeper understanding. Two films might both feature isolated protagonists, but one is a character study about moral ambiguity while the other is melodrama dressed as depth. One uses formal rigor as philosophical statement; the other uses it as style.

## The Solution

**TopFour** analyzes what films *actually believe* — their worldview, technique, philosophical stance — and matches on that basis.

Instead of matching one film at a time, TopFour uses your **Top 4 favorite films** to build a profile of your taste. It extracts the common threads: What worldviews appeal to you? What techniques matter? What do you reject? Then it finds films that align with that taste DNA.

## How It Works

1. **Input your Top 4 films** (incrementally)
2. **System analyzes each** with your input (open-ended clarifying questions)
3. **Generates a taste profile** (poetic description + clinical breakdown)
4. **Get recommendations** based on taste alignment (not individual film matching)
5. **Rate recommendations** with structured feedback
6. **System suggests** adding highly-aligned films to your Top 4

Example recommendation output:
```
Based on your taste profile, [Film X] aligns 89%

Connects through:
✓ Shares worldview on moral ambiguity without resolution
✓ Uses observational technique over exposition
✓ Refuses narrative convenience
✓ Formal discipline as philosophical stance
```

## Why This Matters

- **Deeper matching**: Based on what films *believe*, not what they look like
- **Explainable**: Every recommendation comes with reasoning you can evaluate
- **Personalized**: Learns from your feedback (what you agree/disagree with)
- **Evolving**: Your taste profile improves as you interact with the system

## Project Status

**Phase 1 (In Development):**
- Top 4 onboarding with clarifying questions
- Taste profile generation (poetic + clinical)
- Taste-based film matching
- Structured recommendation feedback
- Suggestion system for Top 4 updates

**Phase 2 (Planned):**
- User accounts
- Shared film database
- Collaborative filtering (find users with similar taste)
- Public profiles

## Tech Stack

- **Python** — Core logic
- **Claude API** — Film analysis and taste profile generation
- **JSON** — Persistent storage
- **CLI** — User interface (Web UI later)

## Setup

```bash
git clone https://github.com/RohanDasguptaUW/TopFour.git
cd TopFour
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY
python -m src.main
```

## Architecture

```
User Input (Top 4)
  → Auto-fetch film data
  → Analyze each film (worldview, technique, tone)
  → Ask clarifying questions (refine understanding)
  → Generate taste profile (poetic + clinical)
  → Match against new films
  → Show connections to Top 4
  → Collect feedback (structured + free-form)
  → Suggest additions to Top 4
```

## Documentation

- **README.md** — This file (overview)
- **TASKS.md** — Detailed development tasks
- **CLAUDE_CODE.md** — Development workflow guide

## Contributing / Feedback

This is currently a personal project. For Phase 2 (collaborative), contributing guidelines will be added.

## License

TBD

