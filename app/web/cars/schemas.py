from pydantic import BaseModel, Field

class CarBase(BaseModel):
    make: str = Field(..., min_length=1)
    model: str | None = None
    year: int | None = None

class CarRead(CarBase):
    """Used for GET responses"""
    id: int
    external_id: str | None = None

    # Pydantic v2: replaces orm_mode
    model_config = {
        "from_attributes": True
    }
