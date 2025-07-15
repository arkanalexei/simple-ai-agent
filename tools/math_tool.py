# Based on https://python.langchain.com/docs/versions/migrating_chains/llm_math_chain/
# TODO: Refactor the math tool for modularity

import math
import numexpr
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing_extensions import TypedDict
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_node import ToolNode

from langchain_core.messages import HumanMessage, SystemMessage

@tool
def calculator(expression: str) -> str:
  """
  Calculate expression using Python's numexpr library.

  Expression should be a single line mathematical expression
  that solves the problem.

  Examples:
      "37593 * 67" for "37593 times 67"
      "37593**(1/5)" for "37593^(1/5)"
  """
  local_dict = {"pi": math.pi, "e": math.e}
  return str(
    numexpr.evaluate(
      expression.strip(),
      global_dict={},  # restrict access to globals
      local_dict=local_dict,  # add common mathematical functions
    )
  )

llm = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
tools = [calculator]
llm_with_tools = llm.bind_tools(tools, tool_choice="any")

class ChainState(TypedDict):
    """LangGraph state."""

    messages: Annotated[Sequence[BaseMessage], add_messages]


async def acall_chain(state: ChainState, config: RunnableConfig):
    response = await llm_with_tools.ainvoke(state["messages"], config)
    return {"messages": [response]}


async def acall_model(state: ChainState, config: RunnableConfig):
    response = await llm.ainvoke(state["messages"], config)
    return {"messages": [response]}


graph_builder = StateGraph(ChainState)
graph_builder.add_node("call_tool", acall_chain)
graph_builder.add_node("execute_tool", ToolNode(tools))
graph_builder.add_node("call_model", acall_model)
graph_builder.set_entry_point("call_tool")
graph_builder.add_edge("call_tool", "execute_tool")
graph_builder.add_edge("execute_tool", "call_model")
graph_builder.add_edge("call_model", END)
chain = graph_builder.compile()

async def run(query: str) -> str:
  state = {"messages": [SystemMessage(content="You are a calculator assistant. Only respond with the final number."), HumanMessage(content=query)]}
  result = await chain.ainvoke(state)
  final_message = result["messages"][-1]
  return final_message.content.strip()