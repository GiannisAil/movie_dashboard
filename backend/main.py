from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from typing import Annotated
from pydantic import BaseModel
from datetime import date
from models import Movie
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# CORS setup for communicating with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_db: list[Movie]

# letterboxd data includes Date,Name,Year,Letterboxd URI.
# We would need to get extra movie data from an external API or database.
temp_db = [
    Movie(id=1, title="The Matrix", year=1999, rating=9, date_watched="2024-02-14", genre=["Action", "Thriller"], director="Wachowski"),
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

@app.post("/api/upload_csv")
async def get_csv(csv_file: UploadFile):
    # print(f"Received file: {csv_file.filename}")
    return {"filename": csv_file.filename}

@app.get("/")
def allok():
    return {"message": "All systems operational!"}