import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	PDFSearchTool,
	SerperDevTool,
	StagehandTool
)



@CrewBase
class ClaritycareCrew:
    """Claritycare crew"""

    
    @agent
    def pdf_data_extraction_specialist(self) -> Agent:
        
        embedding_config_pdfsearchtool = dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model="gpt-4.1",
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model="text-embedding-3-small",
                ),
            ),
        )
        
        return Agent(
            config=self.agents_config["pdf_data_extraction_specialist"],
            tools=[
				PDFSearchTool(config=embedding_config_pdfsearchtool)
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def voice_communication_coordinator(self) -> Agent:
        
        return Agent(
            config=self.agents_config["voice_communication_coordinator"],
            tools=[

            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    
    @agent
    def provider_website_navigator(self) -> Agent:
        
        return Agent(
            config=self.agents_config["provider_website_navigator"],
            tools=[
				SerperDevTool(),
				StagehandTool()
            ],
            reasoning=False,
            inject_date=True,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
        )
    

    
    @task
    def extract_phone_numbers_and_provider_info(self) -> Task:
        return Task(
            config=self.tasks_config["extract_phone_numbers_and_provider_info"],
        )
    
    @task
    def prepare_voice_call_communication(self) -> Task:
        return Task(
            config=self.tasks_config["prepare_voice_call_communication"],
        )
    
    @task
    def locate_and_open_provider_chat_interface(self) -> Task:
        return Task(
            config=self.tasks_config["locate_and_open_provider_chat_interface"],
        )
    
    @task
    def finalize_communication_setup(self) -> Task:
        return Task(
            config=self.tasks_config["finalize_communication_setup"],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the Claritycare crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
