from hw1.crew import Hw1
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def run():
    crew = Hw1().crew()
    result = crew.kickoff()
    print("\n=== OUTPUT ===\n")
    print(result)

if __name__ == "__main__":
    run()