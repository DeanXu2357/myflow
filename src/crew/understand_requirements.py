import json
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI
from langchain.llms import Ollama
from pydantic import BaseModel
from typing import List, Optional


# 定義資料模型
class UnderstandRequirements(BaseModel):
    program_lang: str
    project_path: str
    librarys: List[str]
    implementations: Optional[str]
    expect: str

    def kickoff(self, state):
        # 創建 OpenAI 語言模型
        llm = Ollama(model="llama3")

        # 定義代理
        information_collector = Agent(
            role="Information Collector",
            goal="Collect all necessary project information from the user and output in JSON format",
            backstory="""You are an expert in gathering project requirements. Your task is to interact with the user and collect all necessary information for the project. You must output the collected information in a valid JSON format.""",
            verbose=True,
            llm=llm,
        )

        information_validator = Agent(
            role="Information Validator",
            goal="Validate and confirm the collected project information, maintaining JSON format",
            backstory="""You are an expert in validating project requirements. 
                        Your task is to ensure all collected information is complete, consistent, and clear. 
                        You must maintain the JSON format in your output.""",
            verbose=True,
            llm=llm,
        )

        prompt_optimizer = Agent(
            role="AI Prompt Engineering Specialist",
            goal="Create an optimized, clear, and actionable prompt based on project requirements",
            backstory="""You are a world-renowned AI prompt engineering specialist with years of experience in crafting perfect prompts for various AI models. Your expertise lies in distilling complex project requirements into concise, effective prompts that guide AI systems to produce outstanding results. You have a keen understanding of how different phrasings and structures can significantly impact AI output.""",
            verbose=True,
            llm=llm,
        )

        # 定義任務
        collect_info_task = Task(
            description="""
                Interact with the user to collect the following information:
                1. Programming language (program_lang)
                2. Project's absolute path on local machine (project_path)
                3. Libraries and frameworks to be used (librarys)
                4. Implementation scope (implementations) - optional
                5. Expected goals and results (expect)
    
                Format the collected information as a JSON object with these exact keys.
                Ensure that the 'librarys' field is a JSON array of strings.
                Your output must be a valid JSON object. Here's an example of the expected format:
    
                {
                    "program_lang": "Python",
                    "project_path": "/home/user/projects/my_project",
                    "librarys": ["numpy", "pandas", "scikit-learn"],
                    "implementations": "Implement a machine learning model for predicting stock prices",
                    "expect": "A working model with 85% accuracy and a web interface for user input"
                }
    
                Do not include any other text or explanation in your response, only the JSON object.
            """,
            agent=information_collector,
        )

        validate_info_task = Task(
            description="""
            Validate the collected information:
            1. Ensure all required fields are present
            2. Check for consistency and clarity
            3. Identify any potential issues or missing details
    
            If any issues are found, interact with the user to resolve them.
            Return the validated information as a JSON object, maintaining the exact keys from the input.
            Your output must be a valid JSON object without any additional text or explanation.
            """,
            agent=information_validator,
        )

        optimize_prompt_task = Task(
            description="""
            Role-play: You are an AI Prompt Engineering Specialist tasked with creating the perfect prompt for an AI system that will assist in developing a software project.
            
            Your mission:
            1. Carefully analyze the provided project information, including:
               - Programming language
               - Project scope
               - Expected outcomes
               - Technical requirements
               - Any other relevant details

            2. Craft an optimized prompt that:
               - Captures the essence of the project
               - Is clear, concise, and highly actionable
               - Provides enough context for the AI to understand the project's needs
               - Encourages creative and efficient solutions
               - Addresses potential challenges or constraints

            3. Ensure your prompt:
               - Uses professional, technical language appropriate for software development
               - Is written entirely in English
               - Avoids ambiguity and vagueness
               - Includes specific details from the project requirements

            4. Format your response:
               - Begin with "Optimized Prompt:" followed by your crafted prompt
               - Do not include any other text, explanations, or JSON formatting

            Remember, your expertise in prompt engineering is crucial for the success of this project. The quality of your prompt will directly impact the AI's ability to assist in the software development process.
             """,
            agent=prompt_optimizer,
        )

        # 創建 Crew
        project_requirements_crew = Crew(
            agents=[information_collector, information_validator, prompt_optimizer],
            tasks=[collect_info_task, validate_info_task, optimize_prompt_task],
            verbose=2,
        )

        # 執行 Crew
        result = project_requirements_crew.kickoff()

        result_dict = json.loads(result)
        return {**state, "requirements": result_dict}