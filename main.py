from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from agent import classify_tool
from tools import math_tool, weather_tool, llm_tool

load_dotenv()

app = FastAPI()


class QueryRequest(BaseModel):
  query: str

@app.post("/query")
async def handle_query(request: QueryRequest):
  tool_used = classify_tool(request.query)
  
  if tool_used == "math":
    result = math_tool.run(request.query)
    
    if "Error" in result:  # Fallback to LLM if math fails
      tool_used = "llm"
      result = llm_tool.run(request.query)
      
  elif tool_used == "weather":
    result = weather_tool.run(request.query)
  else:
    result = llm_tool.run(request.query)
  
  return {
    "query": request.query,
    "tool_used": tool_used,
    "result": result
  }

