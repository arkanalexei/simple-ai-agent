from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from tools import math_tool, weather_tool, llm_tool

app = FastAPI()


class QueryRequest(BaseModel):
  query: str
  tool: Optional[str] = None # temporary, to test tool usage

@app.post("/query")
async def handle_query(request: QueryRequest):
  tool_used = request.tool if request.tool else "none"
  
  if tool_used == "math":
    result = math_tool.run(request.query)
  elif tool_used == "weather":
    result = weather_tool.run(request.query)
  elif tool_used == "llm":
    result = llm_tool.run(request.query)
  else:
    result = "Tool not used yet"
  
  return {
    "query": request.query,
    "tool_used": tool_used,
    "result": result
  }

