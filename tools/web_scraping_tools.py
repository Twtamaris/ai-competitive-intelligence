# tools/web_scraping_tools.py
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from requests_html import HTMLSession
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, wait_random
import time
from typing import List, Optional

# Input schema for the scraping tool
class ScrapeInput(BaseModel):
    url: str = Field(description="The URL of the webpage to scrape.")

class WebScrapingTool(BaseTool):
    name = "Web Scraper"
    description = "Useful for extracting the main text content from a given URL. " \
                  "Input should be a single URL string."
    args_schema: type[BaseModel] = ScrapeInput

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=3),
           retry=retry_if_exception_type(Exception), reraise=True) # Reraise exception after retries
    def _scrape_single_url(self, url: str) -> str:
        """Helper to scrape content from a single URL with retries."""
        session = HTMLSession()
        try:
            # Added a sleep for polite scraping and to avoid aggressive rate limiting
            time.sleep(0.5)
            r = session.get(url, timeout=20) # Add timeout for requests
            r.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

            # Optional: Render JavaScript if needed. Be cautious, this can be slow.
            # r.html.render(timeout=30, sleep=2)

            # Try to find common content areas or fall back to body text
            content_elements = r.html.find('article, main, .content, #content, body')
            if content_elements:
                # Join text from found elements, ensuring uniqueness and order
                unique_content = []
                for el in content_elements:
                    text = el.text.strip()
                    if text and text not in unique_content:
                        unique_content.append(text)
                content = "\n\n".join(unique_content)
            else:
                content = r.html.html.full_text # Fallback to full text if specific elements not found

            # Limit content length to avoid exceeding LLM context window
            return content[:10000] # Adjust as needed, max is typically 128k but smaller is safer
        except Exception as e:
            raise Exception(f"Failed to scrape content from {url}: {e}") # Re-raise for retry to catch
        finally:
            session.close() # Ensure session is closed

    def _run(self, url: str) -> str:
        """
        Use the tool to scrape content from a single URL.
        This method is called by the LangChain agent.
        """
        try:
            return self._scrape_single_url(url)
        except Exception as e:
            return f"Error: Could not scrape content from {url}. Reason: {e}"

    async def _arun(self, url: str) -> str:
        """Async version of the tool (optional for simple sync setup)."""
        # For simplicity, we'll just call the sync version for now.
        return self._run(url)

# Instantiate the tool
get_web_scraping_tool = WebScrapingTool()