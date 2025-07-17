from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from agent import classify_tool
from tools import llm_tool, math_tool, weather_tool
from utils.errors import AppError
from utils.llm import get_llm
from utils.logging import get_logger

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


ws_logger = get_logger("llm_websocket")


@app.websocket("/ws/llm")  # type: ignore[misc]
async def llm_stream(websocket: WebSocket) -> None:
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            ws_logger.info(f"Received data: {data}")

            llm = get_llm()
            full_response = ""

            async for chunk in llm.astream(data):
                content = getattr(chunk, "content", None)
                if content:
                    full_response += content
                    await websocket.send_text(content)

            ws_logger.info(f"Full response: {full_response}")
            await websocket.send_text("Stream completed")

    except WebSocketDisconnect:
        ws_logger.info("WebSocket disconnected")

    except Exception as e:
        ws_logger.error(f"Error in WebSocket: {e}")
        await websocket.send_text("Error")
