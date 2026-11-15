from pydantic import (
    BaseModel,
    Field
)


class Pagination(BaseModel):
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=1)
    total: int = Field(ge=0, default=0)
    total_pages: int = Field(ge=0, default=1)