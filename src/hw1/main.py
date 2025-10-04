from hw1.crew import Hw1
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def run_with_prompt(user_prompt: str | None = None):
    crew = Hw1().crew()
    inputs = {"user_prompt": user_prompt or ""}
    result = crew.kickoff(inputs=inputs)
    print("\n=== OUTPUT ===\n")
    print(result)
    return str(result)

def run():
    # Backward-compatible entry with no external prompt
    run_with_prompt("")

if __name__ == "__main__":
    run()