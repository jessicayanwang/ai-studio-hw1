# Hw1/Hw2 Crew

Welcome to the **Hw1 Crew** project, powered by [crewAI](https://crewai.com).  
This project demonstrates a simple multi-agent AI system that introduces the user to a class using **two agents** and **two tasks**.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project includes a `requirements.txt` file that lists all required packages. You can install them with:
```bash
pip install -r requirements.txt
```
Alternatively, if you’re using UV (recommended for speed and reproducibility):
```bash
pip install uv
crewai install
```

## Setup

1. Add your `OPENAI_API_KEY` into the `.env` file.
2. Add your resume to the knowledge/ folder (currently Jessica's resume is included as an example - replace it with your own to personalize the intro).
3. To remove previously stored knowledge, run:
```bash
crewai reset-memories --knowledge
```
   
## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```
or
```bash
$ python src/hw1/main.py
```

Both commands will assemble your crew and execute the tasks as defined in your configuration.


## Crew Design: 2 Agents + 2 Tasks

This project uses a simple pipeline:

- **Agent 1 – Profile Selector**  
  Extracts the most relevant details about the user (name, program, background, interests, fun detail).

- **Agent 2 – Script Writer**  
  Takes the outline from Agent 1 and generates a friendly 2–3 sentence self-introduction, saving it to `intro.md`.

**Tasks:**

1. **Build Outline** – Profile Selector creates a bullet-point outline from the user profile.  
2. **Write Script** – Script Writer converts the outline into a short intro and writes it to file.  

## Reflection

Reflection document is stored in `reflection.md`.

---
## HW2 Extension: Connected Agent Using the Nanda Adapter SDK
1. Setup EC2 perms and Anthropic API key.
2. Install Nanda.
3. To run the project:
```bash
nohup python3 ai-studio-hw1/nanda_crewai.py > out.log 2>&1 &
```
3. To check the output
```bash
cat out.log
```


---

## Support

For support, questions, or feedback regarding the Hw1 Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
