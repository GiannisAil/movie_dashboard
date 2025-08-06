from fastapi import FastAPI, Query, HTTPException
from typing import Annotated
from pydantic import BaseModel
from datetime import date
from models import Movie


app = FastAPI()

temp_db: list[Movie]
temp_db = [
    Movie(id=1, title="The Matrix", year=1999, rating=9, date_watched="2024-02-14", genre=["Action"], director="Wachowski"),
    Movie(id=2, title="La La Land", year=2016, rating=8, date_watched="2024-03-02", genre=["Musical"], director="Chazelle")
]

@app.get("/api/movies", response_model=list[Movie])
def get_movies():
    return temp_db

@app.post("/api/movies", response_model=Movie)
def add_movie(movie: Movie):
    # check if movie already exists in temp_db
    if movie.id in [x.id for x in temp_db]:
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")
    else:
        temp_db.append(movie)
    return movie