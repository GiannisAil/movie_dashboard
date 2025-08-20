from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from typing import Annotated
from pydantic import BaseModel
from datetime import date
from models import Movie as MovieModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from tmdbv3api import TMDb, Search, Movie
import constants 

app = FastAPI()

tmdb = TMDb()
tmdb.language = 'en'
tmdb.api_key = constants.TMDB_API_KEY

api_search = Search()
id_search = Movie()

# TMDB genre IDs to genre names
genreId = { 28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime", 99: "Documentary", 
           18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music", 
           9648: "Mystery", 10749: "Romance", 878: "Science Fiction", 10770: "TV Movie", 53: "Thriller", 
           10752: "War", 37: "Western" }


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

    csv_df = pd.read_csv(csv_file.file)

    # populate user's csv with extra data from the tmdb api
    enriched = []
    for _, row in csv_df.iterrows():
        title = row.get("Name")
        year = row.get("Year")
        tmdb_data = api_search.movies(str(title), year=int(year))
        tmdb_data = tmdb_data[0] # get the first result, since we are using title + release year
        movie_data = id_search.details(tmdb_data["id"], append_to_response="casts") if tmdb_data else None # we can maybe use append to response here to get director

        enriched.append({
            "name": title,
            "year": year,
            "tmdb_id": tmdb_data["id"] if tmdb_data else None,
            "poster": f"https://image.tmdb.org/t/p/w500{tmdb_data['poster_path']}" if tmdb_data and tmdb_data.get("poster_path") else None,
            "overview": tmdb_data.get("overview") if tmdb_data else None,
            "release_date": tmdb_data.get("release_date") if tmdb_data else None,
            "vote_average": tmdb_data.get("vote_average") if tmdb_data else None,
            "genre_ids": tmdb_data.get("genre_ids") if tmdb_data else None,
            "budget": movie_data.budget if movie_data else None,
            "original_language": movie_data.original_language if movie_data else None,
            "runtime": movie_data.runtime if movie_data else None,
            "revenue": movie_data.revenue if movie_data else None, 
            "director": next((c.name for c in movie_data.casts.crew if c.job == "Director"), None) if movie_data else None,
        })
    
    
    df = pd.DataFrame(enriched)


    # number of movies watched
    movie_num = len(df)

    # find the oldest movie watched, check for day/month after tmdb api integration
    oldest = df.loc[df['year'].idxmin()]
    oldest_year = oldest['year'].item()
    oldest_name = oldest['name']

    # find the newest movie watched
    newest = df.loc[df['year'].idxmax()]
    newest_year = newest['year'].item()
    newest_name = newest['name']

    # average release year
    average_year = df['year'].mean()
    average_year = round(average_year)

    # get favorite genres
    df_genres = df.explode('genre_ids')
    genre_counts = df_genres['genre_ids'].value_counts()
    favorite_genres = genre_counts.head(5).to_dict() # these are the top 5 genres, dict doesn't keep order

    # return most watched director 
    # movies watched per year 
    # actor/actress stats
    # most active month 
    # movies watched per weekday
    # average movie length / longest / shortest 

    print(genre_counts.to_string()) #test, it works

    return {"count": movie_num, 
            "oldest_movie": {"name": oldest_name, "year": oldest_year},
            "newest_movie": {"name": newest_name, "year": newest_year},
            "average_year": average_year,
            "favorite_genres": favorite_genres,
            }

@app.get("/")
def allok():
    # search = movie.search("Memories of murder") # tmdb api test 
    search = api_search.movies("Memories of murder", year=2003)
    print(search[0])
    return {"message": "All systems operational!"}
