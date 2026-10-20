from fastapi import APIRouter, HTTPException
from app.schemas.service import ServicesResponse, ServicesSummary, Service, ServiceCreate
from app.monitoring import get_system_metrics

router = APIRouter()

services = [
    {
        "id": 1,
        "name": "Game Server",
        "type": "game-server",
        "status": "online",
        "host": "127.0.0.1",
    },
    {
       "id": 2,
               "name": "Web API",
               "type": "api",
               "status": "online",
               "host": "127.0.0.1", 
    },
    {
        "id": 3,
                "name": "Database",
                "type": "database",
                "status": "unknown",
                "host": "127.0.0.1",
    },
]

@router.get("/services", response_model=ServicesResponse)
def get_services():
    return {
        "items": services,
        "total": len(services)
    }

@router.get("/services/summary", response_model=ServicesSummary)
def get_services_summary():
    online = 0
    offline = 0
    unknown = 0

    for service in services:
        if service["status"] == "online":
            online += 1
        elif service["status"] == "offline":
            offline += 1
        elif service["status"] == "unknown":
            unknown += 1

    return {
        "total": len(services),
        "online": online,
        "offline": offline,
        "unknown": unknown,
    }

@router.post("/services", response_model=Service, status_code=201)
def create_service(new_service: ServiceCreate):
    service_data = new_service.model_dump()

    service_data["id"] = max (
        (service["id"] for service in services),
        default=0,
    ) + 1

    services.append(service_data)

    return service_data

@router.get("/services/{service_id}", response_model=Service)
def get_service(service_id: int):
    for service in services:
        if service["id"] == service_id:
            return service

    raise HTTPException(
        status_code=404,
        detail="Service not found",
    )

@router.get("/metrics")
def read_system_metrics():
    return get_system_metrics()