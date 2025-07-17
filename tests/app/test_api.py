from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_handle_query_mocked() -> None:
    with patch("main.classify_tool", return_value="math"):
        response = client.post("/query", json={"query": "2 + 2"})
        assert response.status_code == 200
        data = response.json()
        assert data["tool_used"] == "math"
        assert data["result"] == "4"
