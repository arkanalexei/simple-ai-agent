# 🧠 Simple AI Agent

![System Architecture](assets/architecture.png)

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
- Dockerized app for easy deployment anywhere


## 📦 Requirements

- Python 3.12
- [OpenAI API key](https://platform.openai.com/account/api-keys)
- [OpenWeatherMap API key](https://openweathermap.org/api)


## 🛠️ Setup

```bash
git clone https://github.com/arkanalexei/simple-ai-agent.git
cd simple-ai-agent
python -m venv env
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

## ✅ Running Tests 

Tests are located under the `tests/` directory, organized by tool/module.

To run all tests with coverage report:
```bash
pytest --cov --cov-report term-missing
```


This project has extensive automated tests covering tool logic, classification, error handling, and API behavior.

| Module                      | Coverage |
|----------------------------|----------|
| `agent.py`                 | 86%      |
| `main.py`                  | 93%      |
| `tools/`                   | 100%     |
| `utils/`                   | 100%     |
| `tests/`                   | 100%     |
| **Total**                  | **99%**  |

All 26 tests pass. Code paths, edge cases, and failures are tested using `pytest`, `pytest-asyncio`, and `unittest.mock`.

