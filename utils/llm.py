from langchain_openai import ChatOpenAI


def get_llm(model: str = "gpt-4.1-nano", temperature: float = 0) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)
