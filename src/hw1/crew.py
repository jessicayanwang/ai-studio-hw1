# src/hw1/crew.py
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

@CrewBase
class Hw1():
    """Two-agent intro crew: Profile Selector -> Script Writer"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # --- Agents ---
    @agent
    def profile_selector(self) -> Agent:
        # Uses config from config/agents.yaml under key 'profile_selector'
        return Agent(
            config=self.agents_config['profile_selector'],  
            verbose=True
        )

    @agent
    def script_writer(self) -> Agent:
        # Uses config from config/agents.yaml under key 'script_writer'
        return Agent(
            config=self.agents_config['script_writer'],  
            verbose=True
        )

    # --- Tasks ---
    @task
    def build_outline(self) -> Task:
        # Uses config from config/tasks.yaml under key 'build_outline'
        return Task(
            config=self.tasks_config['build_outline'], 
        )

    @task
    def write_script(self) -> Task:
        # Uses config from config/tasks.yaml under key 'write_script'
        # Writes the final 2–3 sentence intro to intro.md
        return Task(
            config=self.tasks_config['write_script'],  
            output_file='intro.md'
        )

    # --- Crew ---
    @crew
    def crew(self) -> Crew:
        profile_source = PDFKnowledgeSource(
            file_paths=["resume_Jessica_Wang.pdf"]
        )


        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            knowledge_sources=[profile_source], 
        )