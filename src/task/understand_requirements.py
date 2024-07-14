from crewai import Agent, Task, Crew
from langchain.llms import OpenAI
from pydantic import BaseModel
from typing import List, Optional

# 定義資料模型
class ProjectRequirements(BaseModel):
    program_lang: str
    project_path: str
    repository_url: str
    librarys: List[str]
    implementations: Optional[str]
    expect: str

    def kickoff(self, state):
        # 創建 OpenAI 語言模型
        llm = OpenAI(temperature=0.7)

        # 定義代理
        information_collector = Agent(
            role='Information Collector',
            goal='Collect all necessary project information from the user',
            backstory='You are an expert in gathering project requirements. Your task is to interact with the user and collect all necessary information for the project.',
            verbose=True,
            llm=llm
        )

        information_validator = Agent(
            role='Information Validator',
            goal='Validate and confirm the collected project information',
            backstory='You are an expert in validating project requirements. Your task is to ensure all collected information is complete, consistent, and clear.',
            verbose=True,
            llm=llm
        )

        prompt_optimizer = Agent(
            role='Prompt Optimizer',
            goal='Optimize the prompt based on the implementation scope and expected results',
            backstory='You are an expert in creating optimal prompts for AI models. Your task is to refine the prompt based on the project\'s implementation scope and expected results.',
            verbose=True,
            llm=llm
        )

        # 定義任務
        collect_info_task = Task(
            description='''
            Interact with the user to collect the following information:
            1. Programming language (program_lang)
            2. Project's absolute path on local machine (project_path)
            3. Project repository URL (repository_url)
            4. Libraries and frameworks to be used (librarys)
            5. Implementation scope (implementations) - optional
            6. Expected goals and results (expect)

            Format the collected information as a JSON object.
            ''',
            agent=information_collector
        )

        validate_info_task = Task(
            description='''
            Validate the collected information:
            1. Ensure all required fields are present
            2. Check for consistency and clarity
            3. Identify any potential issues or missing details

            If any issues are found, interact with the user to resolve them.
            Return the validated information as a JSON object.
            ''',
            agent=information_validator
        )

        optimize_prompt_task = Task(
            description='''
            Based on the implementation scope and expected results:
            1. Analyze the provided information
            2. Create an optimized prompt that captures the essence of the project
            3. Ensure the prompt is clear, concise, and actionable

            Return the optimized prompt along with the original project information.
            ''',
            agent=prompt_optimizer
        )

        # 創建 Crew
        project_requirements_crew = Crew(
            agents=[information_collector, information_validator, prompt_optimizer],
            tasks=[collect_info_task, validate_info_task, optimize_prompt_task],
            verbose=2
        )

        # 執行 Crew
        result = project_requirements_crew.kickoff()

        return {**state, "requirements": result}

