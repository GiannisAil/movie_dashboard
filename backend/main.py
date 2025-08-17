from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from typing import Annotated
from pydantic import BaseModel
from datetime import date
from models import Movie as MovieModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from tmdbv3api import TMDb, Movie
import constants 

app = FastAPI()

tmdb = TMDb()
tmdb.language = 'en'
tmdb.api_key = constants.TMDB_API_KEY

movie = Movie()

# CORS setup for communicating with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

temp_db: list[MovieModel]

# letterboxd data includes Date,Name,Year,Letterboxd URI.
# We would need to get extra movie data from an external API or database.
temp_db = [
    MovieModel(id=1, title="The Matrix", year=1999, rating=9, date_watched="2024-02-14", genre=["Action", "Thriller"], director="Wachowski"),
    MovieModel(id=2, title="La La Land", year=2016, rating=8, date_watched="2024-03-02", genre=["Musical"], director="Chazelle")
]

@app.get("/api/movies", response_model=list[MovieModel])
def get_movies():
    return temp_db

@app.post("/api/movies", response_model=MovieModel)
def add_movie(movie: MovieModel):
    # check if movie already exists in temp_db
    if movie.id in [x.id for x in temp_db]:
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")
    else:
        temp_db.append(movie)
    return movie

@app.post("/api/upload_csv")
async def get_csv(csv_file: UploadFile):
    # print(f"Received file: {csv_file.filename}")

    df = pd.read_csv(csv_file.file)

    # populate user's csv with extra data from the tmdb api

    # number of movies watched
    movie_num = len(df)

    # find the oldest movie watched, check for day/month after tmdb api integration
    oldest = df.loc[df['Year'].idxmin()]
    oldest_year = oldest['Year'].item()
    oldest_name = oldest['Name'] 

    # find the newest movie watched
    newest = df.loc[df['Year'].idxmax()]
    newest_year = newest['Year'].item()
    newest_name = newest['Name']

    # average release year
    average_year = df['Year'].mean()
    average_year = round(average_year)

    # return most watched director 
    # movies watched per year 
    # top genres
    # actor/actress stats
    # most active month 
    # movies watched per weekday
    # average movie length / longest / shortest 

    return {"count": movie_num, 
            "oldest_movie": {"name": oldest_name, "year": oldest_year},
            "newest_movie": {"name": newest_name, "year": newest_year},
            "average_year": average_year
            }

@app.get("/")
def allok():
    search = movie.search("Memories of murder") # tmdb api test 
    for res in search:
        print(f"Title: {res.title}, Release Date: {res.release_date}, Overview: {res.overview}")
    return {"message": "All systems operational!"}