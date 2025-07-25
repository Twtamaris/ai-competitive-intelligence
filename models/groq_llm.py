# models/groq_llm.py
from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY, GROQ_MODEL_NAME

def get_groq_llm(temperature: float = 0.5):
    """
    Initializes and returns a ChatGroq LLM instance.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL_NAME,
        temperature=temperature
    )

# Example of how to get different LLM instances for agents
def get_llm_for_search():
    return get_groq_llm(temperature=0.7) # Higher temperature for more varied search queries if needed

def get_llm_for_summarization():
    return get_groq_llm(temperature=0.3) # Lower temperature for factual summarization

def get_llm_for_verification():
    return get_groq_llm(temperature=0.1) # Very low temperature for strict verification

def get_llm_for_coordination():
    return get_groq_llm(temperature=0.0) # Zero temperature for strict orchestration