from fastapi import APIRouter
from app.schemas.service import ServicesResponse, ServiceSummary

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

@router.get("/services/summary", response_model=ServiceSummary)
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