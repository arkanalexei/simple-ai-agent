from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from agent import classify_tool
from tools import llm_tool, math_tool, weather_tool
from utils.errors import AppError

load_dotenv()

app = FastAPI()


class QueryRequest(BaseModel):  # type: ignore[misc]
    query: str


@app.post("/query")  # type: ignore[misc]
async def handle_query(request: QueryRequest) -> dict[str, str | None]:
    try:
        tool_used = classify_tool(request.query)

        if tool_used == "math":
            result = await math_tool.run(request.query)
        elif tool_used == "weather":
            result = await weather_tool.run(request.query)
        else:
            result = await llm_tool.run(request.query)

        return {"query": request.query, "tool_used": tool_used, "result": result}
    except AppError as e:
        return {"query": request.query, "tool_used": "none", "result": None, "error": str(e)}
