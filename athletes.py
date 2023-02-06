from pydantic import BaseModel, Field
from uuid import UUID
class Athlete(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=100)
    license: str = Field(min_length=2, max_length=30)
    birthday: str = Field(min_length=10, max_length=10) #12/10/2004
    category: str = Field(min_length=3, max_length=30)

