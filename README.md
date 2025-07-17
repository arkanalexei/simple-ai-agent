# 🧠 Simple AI Agent

A lightweight FastAPI-based backend that routes natural language queries to the appropriate tool:
- 🧮 Math calculator
- 🌤️ Weather checker
- 💬 General knowledge via LLM

## 🚀 Features

- Natural language query classification using LLM
- Tool routing via LangChain & LangGraph
- Weather tool with city extraction + OpenWeatherMap API
- Math tool using secure expression evaluation
- LLM tool for open-ended questions (uses OpenAI)
- WebSocket streaming endpoint for real-time LLM responses
- Error handling and logging included


## 📦 Requirements

- Python 3.12
- OpenAI API key
- OpenWeatherMap API key


## 🛠️ Setup

```bash
git clone https://github.com/arkanalexei/simple-ai-agent.git
cd simple-ai-agent
python -m venv eenv
source env/bin/activate  # or env\Scripts\activate on Windows
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file (you can copy from `.env.example`):

```
OPENAI_API_KEY=
OPENWEATHERMAP_API_KEY=
```

## 🏃 Running the Server

```bash
uvicorn main:app --reload
```

Server will be available at `http://localhost:8000`

## 📮 HTTP API Usage

### `POST /query`

**Request 1:**

```json
{
  "query": "What is 42 * 7?"
}
```

**Response 1:**

```json
{
  "query": "What is 42 * 7?",
  "tool_used": "math",
  "result": "294"
}
```

**Request 2:**

```json
{
  "query": "What's the weather today in Jakarta?"
}
```

**Response 2:**

```json
{
  "query": "What's the weather today in Jakarta?",
  "tool_used": "weather",
  "result": "It's clear sky and 30.35°C in Jakarta."
}
```

---

## 🔄 WebSocket Streaming (LLM only)

### `GET ws://localhost:8000/ws/llm`

* Connect with Postman or any WebSocket client.
* Send plain text query like:

  ```
  Tell me a fun fact about cats.
  ```
* Receive streamed responses chunk by chunk.
* Ends with:

  ```
  Stream completed
  ```

## 🐳 Docker

```bash
docker build -t simple-ai-agent .
docker run -p 8000:8000 --env-file .env simple-ai-agent
```