from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "gameops-api",
        "version": "0.1.0",
    }

def test_services_list():
    response = client.get("/api/v1/services")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert len(data["items"]) == 3

def test_services_fields():
    response = client.get("/api/v1/services")
    services = response.json()["items"]

    for service in services:
        assert "id" in service
        assert "name" in service
        assert "type" in service
        assert "status" in service
        assert "host" in service

def test_service_status_is_valid():
    response = client.get("/api/v1/services")
    services = response.json()["items"]

    allowed_statuses = {"online", "offline", "unknown"}

    for service in services:
        assert service["status"] in allowed_statuses

def test_services_response_matches_schema():
    from app.schemas.service import ServicesResponse

    response = client.get("/api/v1/services")

    assert response.status_code == 200

    data = ServicesResponse.model_validate(response.json())

    assert data.total == len(data.items)

def test_services_summary():
    response = client.get("/api/v1/services/summary")

    assert response.status_code == 200
    assert response.json() == {
        "total": 3, 
        "online": 2,
        "offline": 0,
        "unknown": 1,
    }

def test_create_service():
    from app.api.routes import services

    original_services = services.copy()

    try:
        response = client.post(
            "/api/v1/services",
            json={
                "name": "Test Service",
                "type": "api",
                "status": "online",
                "host": "127.0.0.1",
            },
        )

        assert response.status_code == 201

        created_service = response.json()

        assert created_service["id"] == 4
        assert created_service["name"] == "Test Service"
        assert created_service["status"] == "online"

        list_response = client.get("/api/v1/services")
        assert list_response.status_code == 200
        assert list_response.json()["total"] == 4

    finally:
        services[:] = original_services

def test_create_service_rejects_blank_name():
    response = client.post(
        "/api/v1/services",
        json={
            "name": "   ",
            "type": "api",
            "status": "online",
            "host": "127.0.0.1",
        },
    )

    assert response.status_code == 422

def test_create_service_rejects_invalid_status():
    response = client.post(
        "/api/v1/services",
        json={
            "name": "Test Service",
            "type": "api",
            "status": "broken",
            "host": "127.0.0.1",
        },
    )

    assert response.status_code == 422

def test_get_service_by_id():
    response = client.get("/api/v1/services/1")

    assert response.status_code == 200

    service = response.json()

    assert service["id"] == 1
    assert service["name"] == "Game Server"

def test_get_service_not_found():
    response = client.get("api/v1/services/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"