"""
Film Worldview Recommender - Main CLI
======================================

Usage:
    python -m src.main

This is the entry point for the film recommendation agent.
Use Claude Code to build out the actual functionality.
"""

from src.utils.config import DEBUG


def main():
    """Main CLI loop."""
    print("\n" + "="*70)
    print("FILM WORLDVIEW RECOMMENDER")
    print("="*70 + "\n")
    print("This is a skeleton. Use Claude Code to implement:\n")
    print("1. Film data fetcher (src/data/fetcher.py)")
    print("2. Analysis agent (src/agents/analyzer.py)")
    print("3. Matching logic (src/lib/semantic.py)")
    print("4. Recommendation generation (src/agents/recommender.py)")
    print("5. Storage/caching (src/data/storage.py)")
    print("\nThen this CLI will actually work.\n")
    
    while True:
        try:
            film = input("\n> Recommend based on film: ").strip()
            
            if not film or film.lower() == "quit":
                print("Goodbye.")
                break
            
            n = input("> Top N recommendations (default 3): ").strip()
            try:
                n = int(n) if n else 3
            except ValueError:
                n = 3
            
            # This is where the agent logic goes
            print(f"\n[TODO] Analyze '{film}' and find {n} recommendations")
            print("(Claude Code should implement this)\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye.")
            break
        except Exception as e:
            if DEBUG:
                raise
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
