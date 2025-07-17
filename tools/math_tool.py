# Based on https://python.langchain.com/docs/versions/migrating_chains/llm_math_chain/

from typing import Annotated, Dict, Sequence

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.tool_node import ToolNode
from typing_extensions import TypedDict

from tools.math_calculator import calculator
from utils.errors import ToolError
from utils.llm import get_llm
from utils.logging import get_logger

logger = get_logger("math_tool")


class ChainState(TypedDict):
    """LangGraph state."""

    messages: Annotated[Sequence[BaseMessage], add_messages]


async def acall_chain(state: ChainState, config: RunnableConfig) -> Dict[str, list[BaseMessage]]:
    llm = get_llm()
    tools = [calculator]
    llm_with_tools = llm.bind_tools(tools, tool_choice="any")
    response = await llm_with_tools.ainvoke(state["messages"], config)
    return {"messages": [response]}


async def acall_model(state: ChainState, config: RunnableConfig) -> Dict[str, list[BaseMessage]]:
    llm = get_llm()
    response = await llm.ainvoke(state["messages"], config)
    return {"messages": [response]}


def get_chain() -> CompiledStateGraph[ChainState, ChainState, ChainState]:
    tools = [calculator]

    graph_builder = StateGraph(ChainState)
    graph_builder.add_node("call_tool", acall_chain)
    graph_builder.add_node("execute_tool", ToolNode(tools))
    graph_builder.add_node("call_model", acall_model)
    graph_builder.set_entry_point("call_tool")
    graph_builder.add_edge("call_tool", "execute_tool")
    graph_builder.add_edge("execute_tool", "call_model")
    graph_builder.add_edge("call_model", END)
    chain = graph_builder.compile()
    return chain


async def run(query: str) -> str:
    chain = get_chain()
    state = {
        "messages": [
            SystemMessage(
                content="You are a calculator assistant. Only respond with the final number."
            ),
            HumanMessage(content=query),
        ]
    }
    try:
        result = await chain.ainvoke(state)
        final_message = result["messages"][-1]
        return str(final_message.content.strip())
    except Exception as e:
        logger.error(f"Math calculation failed: {str(e)}")
        raise ToolError(f"Math calculation failed: {str(e)}")
