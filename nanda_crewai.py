#!/usr/bin/env python3
import sys, os
from nanda_adapter import NANDA

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from hw1.crew import Hw1

def create_crewai_handler():
    """
    Inbound text -> run your two-task flow (Profile Selector -> Script Writer)
    You can branch on message_text if you want outline-only vs full intro.
    """
    def handle(message_text: str) -> str:
        try:
            crew = Hw1().crew()
            # If you later want modes, inspect message_text here.
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"Error running CrewAI agent: {e}"
    return handle

def main():
    nanda = NANDA(create_crewai_handler())

    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    domain = os.getenv("DOMAIN_NAME")
    if not anthropic_key or not domain:
        raise RuntimeError("Set ANTHROPIC_API_KEY and DOMAIN_NAME before starting the adapter.")

    # Start HTTPS server + register with Nanda
    nanda.start_server_api(anthropic_key, domain)

if __name__ == "__main__":
    main()
