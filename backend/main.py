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
    # enriched = []
    # for _, row in csv_df.iterrows():
    #     title = row.get("Name")
    #     year = row.get("Year")
    #     watch_date = row.get("Date")
    #     tmdb_data = api_search.movies(str(title), year=int(year))
    #     print(str(title))
    #     # print(tmdb_data)
    #     if tmdb_data.get('results'):
    #         # check that the title matched. if the exact title isnt in the results, skip the movie

    #         for result in tmdb_data:
    #             if result.title == str(title):
    #                 tmdb_data = result
    #                 break
    #         else:
    #             continue # if the exact title can't be found, skip the movie. We are doing this to minimize the chance of getting wrong titles

    #         # tmdb_data = tmdb_data[0]
    #         movie_data = id_search.details(tmdb_data["id"], append_to_response="casts") if tmdb_data else None # we can maybe use append to response here to get director
    #         # remove the row if the api search doesn't return anything, it most likely is a tv series
    #     else:
    #         continue

        # enriched.append({
        #     "name": title,
        #     "year": year,
        #     "watch_date": watch_date,
        #     "tmdb_id": tmdb_data["id"] if tmdb_data else None,
        #     "poster": f"https://image.tmdb.org/t/p/w500{tmdb_data['poster_path']}" if tmdb_data and tmdb_data.get("poster_path") else None,
        #     "overview": tmdb_data.get("overview") if tmdb_data else None,
        #     "release_date": tmdb_data.get("release_date") if tmdb_data else None,
        #     "vote_average": tmdb_data.get("vote_average") if tmdb_data else None,
        #     "genre_ids": tmdb_data.get("genre_ids") if tmdb_data else None,
        #     "budget": movie_data.budget if movie_data else None,
        #     "original_language": movie_data.original_language if movie_data else None,
        #     "runtime": movie_data.runtime if movie_data else None,
        #     "revenue": movie_data.revenue if movie_data else None, 
        #     "director": next((c.name for c in movie_data.casts.crew if c.job == "Director"), None) if movie_data else None,
        # })
    
    
    # df = pd.DataFrame(enriched)

    # # Save
    # df.to_pickle("movies_cache.pkl") # save the result from api calls for faster development

    # Load
    df = pd.read_pickle("movies_cache.pkl") 

    df['genre_ids'] = df['genre_ids'].apply(
        lambda x: list(x) if x is not None else []
    )

    # make copy of df, to send to frontend
    df_to_frontend = df.to_dict(orient="records")
    

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

    # get most watched directors
    df_directors = df['director'].value_counts() 
    fav_directors = df_directors.head(5).to_dict()

    # convert date to pandas datetime
    df['watch_date'] = pd.to_datetime(df['watch_date'], errors='coerce')

    # movies watched per year, and which movies
    df['watch_year'] = df['watch_date'].dt.year
    movies_per_year = (
        df.groupby("watch_year")["name"]
        .apply(list)
        .apply(lambda movies: {"count": len(movies), "movies": movies})
        .to_dict()
    )

    # most active months
    df['watch_month'] = df['watch_date'].dt.month
    movies_per_month = df['watch_month'].value_counts().to_dict()

    # movies watched per weekday
    df['watch_weekday'] = df['watch_date'].dt.day_name()
    movies_per_weekday = df['watch_weekday'].value_counts().to_dict()

    #movies watched by year-month pair. to show watching trends
    df['year_month'] = df['watch_date'].dt.to_period('M').astype(str)
    movies_per_year_month = df['year_month'].value_counts().to_dict()

    # average runtime
    average_runtime = df['runtime'].mean()
    average_runtime = round(average_runtime) 

    # longest movie 
    longest_movie = df.loc[df['runtime'].idxmax()]
    longest_movie_name = longest_movie['name']
    longest_movie_runtime = longest_movie['runtime'].item()

    # # shortest movie
    shortest_movie = df.loc[df['runtime'].idxmin()]
    shortest_movie_name = shortest_movie['name']
    shortest_movie_runtime = shortest_movie['runtime'].item()

    # actor/actress stats

    # print(movies_per_year) #test, it works

    stats = {"count": movie_num, 
            "oldest_movie": {"name": oldest_name, "year": oldest_year},
            "newest_movie": {"name": newest_name, "year": newest_year},
            "average_year": average_year,
            "favorite_genres": favorite_genres,
            "favorite_directors": fav_directors,
            "movies_per_year": movies_per_year,
            "movies_per_month": movies_per_month,
            "movies_per_weekday": movies_per_weekday,
            "movies_per_year_month": movies_per_year_month,
            "average_runtime": average_runtime,
            "longest_movie": {"name": longest_movie_name, "runtime": longest_movie_runtime},
            "shortest_movie": {"name": shortest_movie_name, "runtime": shortest_movie_runtime},
            }

    # return {"count": movie_num, 
    #         "oldest_movie": {"name": oldest_name, "year": oldest_year},
    #         "newest_movie": {"name": newest_name, "year": newest_year},
    #         "average_year": average_year,
    #         "favorite_genres": favorite_genres,
    #         "favorite_directors": fav_directors,
    #         "movies_per_year": movies_per_year,
    #         "movies_per_month": movies_per_month,
    #         "movies_per_weekday": movies_per_weekday,
    #         "movies_per_year_month": movies_per_year_month,
    #         "average_runtime": average_runtime,
    #         "longest_movie": {"name": longest_movie_name, "runtime": longest_movie_runtime},
    #         "shortest_movie": {"name": shortest_movie_name, "runtime": shortest_movie_runtime},
    #         }
    # print(df_to_frontend)
    
    
    print(type(df['genre_ids'].iloc[0]))


    return { 
        "stats": stats,
        "movies": df_to_frontend
    }

@app.get("/")
def allok():
    # search = movie.search("Memories of murder") # tmdb api test 
    search = api_search.movies("Memories of murder", year=2003)
    print(search[0])
    return {"message": "All systems operational!"}
