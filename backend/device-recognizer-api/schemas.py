from typing import Optional, List

from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    model: Optional[str] = None
    color: Optional[str] = None
    memory: Optional[str] = None
    storage: Optional[str] = None
    screen_size: Optional[str] = None


class DeviceInfoRequest(BaseModel):
    texts: List[str]


class DeviceInfoResponse(BaseModel):
    info: List[DeviceInfo]
