# Reflection: What Worked, What Didn’t, and What I Learned

## What Worked
- **CrewAI Pipeline Setup**  
  I successfully built a two-agent, two-task pipeline where one agent extracts profile details and the other writes a short self-introduction. The sequential process worked smoothly, and outputs were generated as expected.  

- **File Output**  
  Using `output_file`, the system was able to persist the final self-introduction to a Markdown file (`intro.md`). This made the workflow reproducible and easy to validate.  

- **Integration with Resume**  
  By placing a resume in the `knowledge/` folder, the Profile Selector could leverage structured information to build an outline, reducing manual data entry.  


## What Didn’t Work
- **FileWriterTool Limitations**  
  Using the `FileWriterTool` turned out to be less efficient than directly using `output_file`, because it required extra setup for overwrite behavior when the file already existed. In the end, we opted to rely on `output_file` for simpler file writing.  
- **Crew Memory Persistence**  
  When updating knowledge sources (e.g., replacing the resume in the `knowledge/` folder), the system continued using cached memory. We had to manually reset memory with:  
```bash
crewai reset-memories --knowledge
```

## What I Learned
- **Agent/Task Separation**  
  Keeping responsibilities clear (Profile Selector for data extraction, Script Writer for natural language generation) made the system modular and easy to extend.  
  
- **GenAI + Documentation**
  Using generative AI for coding support is helpful for prototyping and debugging, but it’s equally important to read the official documentation (e.g., crewAI docs and example projects). Documentation often clarifies tool behaviors, configuration details, and pitfalls that GenAI alone might not capture.

---

## Test Run Example

**Retrieved Knowledge**

Additional Information: JESSICA WANG
MachineLearning&DataScience | Harvard M.S. Candidate | Graduation Dec 2025
Available Jan 2026
jessicawang@g.harvard.edu (617)-359-8145
jessicayanwang.github.io  Cambridge, MA, USA
EDUCATION
Harvard University - M.S. Data Science Sep 2024 - Dec 2025 (Expected)
University of Toronto - St. George Sep 2019 - Apr 2024
B.S. Data Science, Minor in Mathematics cGPA: 3.99/4.00
...

**Agent: Profile Selector**

Task: 
Using the profile information provided in the knowledge source, build a structured outline with exactly these fields:
- Name
- Program
- Background
- Interests
- Fun detail
Keep it concise and factual (max 5 bullets)

Final Answer:
- Name: Jessica Wang
- Program: Harvard M.S. candidate in Data Science, expected graduation December 2025
- Background: B.S. in Data Science and Minor in Mathematics from the University of Toronto with a cGPA of 3.99/4.00
- Interests: Machine Learning, Data Analysis, Research, Technical Sales
- Fun detail: Built an augmented reality application on Microsoft HoloLens to assist presenters during Q&A sessions.

**Agent: Script Writer**

Task: 
Using the outline from Task 1, draft a 2–3 sentence self-introduction under 60 words.
It should be natural, clear, and friendly — something Jessica could say out loud to classmates.
Avoid jargon, keep it approachable.

Final Answer:
Hi everyone, I'm Jessica! Currently pursuing my Master's in Data Science at Harvard with a passion for Machine Learning and Technical Sales. Fun fact: I once built an AR app on Microsoft HoloLens to assist presenters during Q&A sessions. Can't wait to learn and grow together!

---
## AI Usage Disclaimer

I used generative AI tools to support this project. Specifically:  
- I came up with the idea and overall design myself.  
- I used AI to help draft parts of the code implementation after deciding on the structure.  
- I used AI to assist with debugging issues and resolving errors during development.  
- I also used AI for polishing documentation, correcting grammar, and improving clarity.  
