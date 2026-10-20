from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class Service(BaseModel):
    id: int
    name: str
    type: str
    status: Literal["online", "offline", "unknown"]
    host: str

class ServicesResponse(BaseModel):
    items: list[Service]
    total: int

class ServicesSummary(BaseModel):
    total: int
    online: int
    offline: int
    unknown: int

class ServiceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: str = Field(min_length=1, max_length=50)
    status: Literal["online", "offline", "unknown"]
    host: str = Field(min_length=1, max_length=255)

    @field_validator("name", "type", "host")
    @classmethod
    def reject_blank_strings(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Поле не должно состоять только из пробелов")
        return value.strip()