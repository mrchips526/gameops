from typing import Literal
from pydantic import BaseModel

class Service(BaseModel):
    id: int
    name: str
    type: str
    status: Literal["online", "offline", "unknown"]
    host: str

class ServicesResponse(BaseModel):
    items: list[Service]
    total: int

class ServiceSummary(BaseModel):
    total: int
    online: int
    offline: int
    unknown: int