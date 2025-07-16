from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from agent import classify_tool
from tools import math_tool, weather_tool, llm_tool
from utils.errors import AppError, ToolError

load_dotenv()

app = FastAPI()


class QueryRequest(BaseModel):
  query: str

@app.post("/query")
async def handle_query(request: QueryRequest):
  try:
    tool_used = classify_tool(request.query)
    
    if tool_used == "math":
      
      try:
        result = await math_tool.run(request.query)
      except ToolError as e:
        tool_used = "llm"
        result = await llm_tool.run(request.query)
        
    elif tool_used == "weather":
      result = await weather_tool.run(request.query)
    else:
      result = await llm_tool.run(request.query)
    
    return {
      "query": request.query,
      "tool_used": tool_used,
      "result": result
    }
  except AppError as e:
    return {
      "query": request.query,
      "tool_used": "none",
      "result": None,
      "error": str(e)
    }

