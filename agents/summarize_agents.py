# agents/summarizer_agent.py
from crewai import Agent
from tools.web_scraping_tools import CustomWebScrapingTools # or WebScrapingTools
from langchain_openai import ChatOpenAI

class SummarizerAgents:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.5)

    def summarizer_agent(self):
        return Agent(
            role='Content Summarizer',
            goal='Extract concise, structured updates (product name, summary, source link, date) from provided web content.',
            backstory="""You are a meticulous analyst, skilled at reading through web pages and distilling key information.
                       You are adept at identifying specific product updates, new features, or significant changes,
                       and formatting them into a clear, actionable summary. You are precise and avoid adding
                       any external information.""",
            verbose=True,
            allow_delegation=False, # This agent performs its own summarization
            tools=[CustomWebScrapingTools.get_scraping_tool()], # Or WebsiteReadTool().run
            llm=self.llm
        )