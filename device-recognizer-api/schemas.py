from typing import Optional

from pydantic import BaseModel


class DeviceInfo(BaseModel):
    model: Optional[str] = None
    color: Optional[str] = None
    memory: Optional[str] = None
    storage: Optional[str] = None
    screen_size: Optional[str] = None
