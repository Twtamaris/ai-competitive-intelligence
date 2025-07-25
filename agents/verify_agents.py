# agents/verifier_agent.py
from crewai import Agent
from langchain_openai import ChatOpenAI

class VerifierAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3) # Lower temp for more factualness

    def verifier_agent(self):
        return Agent(
            role='Information Verifier & Filter',
            goal='Validate the relevance and reliability of product update summaries, filtering out irrelevant or unreliable data.',
            backstory="""You are a critical and skeptical fact-checker. Your primary goal is to ensure the accuracy,
                       relevance, and reliability of all competitive intelligence. You cross-reference information
                       and identify any potential hallucinations or outdated data, ensuring only high-quality
                       insights are presented.""",
            verbose=True,
            allow_delegation=False, # This agent performs its own verification
            llm=self.llm
            # Consider adding a tool here if verification requires further lookup (e.g., a mini search tool for source reputation)
        )