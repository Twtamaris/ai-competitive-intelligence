# agents/coordinator_agent.py
from crewai import Agent
from langchain_openai import ChatOpenAI

class CoordinatorAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2) # Even lower temp for orchestration

    def coordinator_agent(self):
        return Agent(
            role='Intelligence Coordinator & Report Generator',
            goal='Orchestrate the entire competitive intelligence gathering process and compile the final structured report.',
            backstory="""You are the project manager for the competitive intelligence team. You ensure
                       each step of the research process is executed flawlessly, from initial search to final verification.
                       Your ultimate responsibility is to synthesize all validated insights into a coherent,
                       structured report (Markdown or JSON) that is ready for a Product Manager.""",
            verbose=True,
            allow_delegation=True, # Crucial for delegating tasks to other agents
            llm=self.llm
            # This agent doesn't need external tools for now, its tools are the other agents via delegation
        )