
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field


class Events(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    start: datetime = Field(default_factory=datetime.now)
    end: Optional[Union[datetime, str]] = None
    title: str

    model_config = {
        "validate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
        }
    }
