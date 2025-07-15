from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_handle_query():
    response = client.post("/query", json={"query": "What is 2 + 2?"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "What is 2 + 2?"
    assert data["tool_used"] == "none"
    assert data["result"] == "Tool not used yet"