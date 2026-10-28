
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to BugWhisperer AI!"


def test_health_endpoint():
    response = client.get("/api/health/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_rejects_empty_code():
    response = client.post(
        "/api/analyze/",
        json={
            "code": "",
            "error_message": "NameError",
            "conversation_id": None,
        },
    )

    assert response.status_code == 422


def test_analyze_rejects_empty_error_message():
    response = client.post(
        "/api/analyze/",
        json={
            "code": "x = 10",
            "error_message": "",
            "conversation_id": None,
        },
    )

    assert response.status_code == 422


def test_analyze_handles_missing_gemini_api_key(monkeypatch):
    import app.main as main_module

    def fake_analyze(request):
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Configure it in your .env file."
        )

    monkeypatch.setattr(main_module, "analyze_bug", fake_analyze)

    response = client.post(
        "/api/analyze/",
        json={
            "code": "print('hello')",
            "error_message": "Example error",
            "conversation_id": None,
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Gemini API key is not configured. Check your .env file."
    )
