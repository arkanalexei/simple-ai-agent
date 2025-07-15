from tools import llm_tool

def test_dummy_llm():
    result = llm_tool.run("What is the capital of France?")
    assert result == "This is a dummy LLM response to: What is the capital of France?"