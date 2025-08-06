from pydantic import BaseModel
from datetime import date

# Fake database for development. stores data schemas

class Movie(BaseModel):
    id: int
    title: str
    year: int
    rating: int | None
    date_watched: date
    genre: list[str]
    director: str