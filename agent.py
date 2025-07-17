from langchain_core.prompts import PromptTemplate

from utils.llm import get_llm

llm = get_llm()

prompt = PromptTemplate.from_template(
    """
You are a smart classifier. Classify the user's query into one of the following tools:
- "math": if it's a math calculation
- "weather": if it's asking about the weather
- "llm": for general knowledge or open-ended questions

Query: {query}
Tool:
"""
)


def get_chain():
    return prompt | llm


def classify_tool(query: str) -> str:
    """
    Classify the query to determine which tool to use.
    """
    chain = get_chain()
    response = chain.invoke({"query": query})
    response = response.content.strip().lower()

    if response in {"math", "weather", "llm"}:
        return response
    return "llm"
