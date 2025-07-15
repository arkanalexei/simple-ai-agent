from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
  query: str

@app.post("/query")
async def handle_query(request: QueryRequest):
  # Assume for initial development purposes
  # we are not using any tools
  # and just returning the query as is.
  
  return {
    "query": request.query,
    "tool_used": "none",
    "result": "Tool not used yet"
  }

