# agents/search_agent.py
from crewai import Agent
from tools.search_tools import CustomSearchTools # or SearchTools if using SerperDevTool
from langchain_openai import ChatOpenAI # Example LLM

class SearchAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7) # Or your chosen LLM

    def search_agent(self):
        return Agent(
            role='Competitive Intelligence Searcher',
            goal='Find the top 5 most relevant and recent online sources (news, blogs, product updates) for the given product category/topic.',
            backstory="""You are an expert at deep web research, quickly sifting through vast amounts of information to pinpoint
                       the most valuable and up-to-date competitive intelligence. You focus on identifying reliable sources like
                       official company announcements, reputable tech news outlets, and well-known industry blogs.""",
            verbose=True,
            allow_delegation=False, # This agent performs its own search
            tools=[CustomSearchTools.get_search_tool()], # Or SerperDevTool().run
            llm=self.llm
        )