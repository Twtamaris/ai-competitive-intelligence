# tools/search_tools.py
from langchain_community.tools import DuckDuckGoSearch
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Input schema for the search tool
class SearchInput(BaseModel):
    query: str = Field(description="The search query to execute.")
    num_results: int = Field(default=5, description="Number of search results to return.")

class DuckDuckGoSearchTool:
    """
    A wrapper for DuckDuckGoSearch tool to perform web searches.
    """
    def __init__(self):
        # DuckDuckGoSearch uses DuckDuckGoSearchAPIWrapper internally
        self.duckduckgo_search = DuckDuckGoSearch()

    def get_tool(self):
        """Returns a LangChain Tool for DuckDuckGo web search."""
        # Using the .run method of DuckDuckGoSearch directly might be simpler here
        # Or you can define a custom _run method if more control is needed.
        return DuckDuckGoSearch(
            name="DuckDuckGo Search",
            description="Useful for performing general web searches to find "
                        "relevant articles, news, or blog posts about product updates. "
                        "Input should be a string search query.",
            args_schema=SearchInput # Optional, but good practice for structured input
        )

    @staticmethod
    def extract_urls_from_search_results(search_results_string: str, num_urls: int = 5) -> List[str]:
        """
        Parses the raw search results string returned by DuckDuckGoSearch to extract URLs.
        This is a helper function, not a LangChain tool, used by the agent to process tool output.
        """
        urls = []
        # DuckDuckGoSearch usually returns a string where results are separated by "\n\n"
        # Each result typically has "title", "link", "snippet"
        # We'll look for "link:" or "URL:" or similar patterns.
        lines = search_results_string.split('\n')
        for line in lines:
            if line.startswith('link:') or line.startswith('URL:'):
                url = line.split(':', 1)[-1].strip()
                if url and url.startswith('http') and url not in urls: # Basic validation and deduplication
                    urls.append(url)
                    if len(urls) >= num_urls:
                        break
        return urls