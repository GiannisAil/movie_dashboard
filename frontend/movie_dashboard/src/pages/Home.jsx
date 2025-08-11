import { useState, useEffect } from 'react';
import Movie from '../components/Movie';
import { getMovies } from '../services/api';

function Home(){
    // movie data for testing
    let testmovie = {
        "id": 1,
        "title": "The test",
        "year": 2222,
        "rating": 9,
        "date_watched": "2024-02-14",
        "genre": [
          "Action",
          "Thriller"
        ],
        "director": "Wachowski"
    }

    const [movie, setMovie] = useState(null);

    useEffect(() => {
        let ignore = false;

        async function fetchMovies(){
            const movies = await getMovies();
            if(!ignore){
                setMovie(movies[0]);
            }
        }
        fetchMovies();
        
        return () => {
            ignore = true; // Cleanup
        };

    }, []);

    
    return (
        <div>
            <h1>Movie Dashboard</h1>
            <h3>Your Movies:</h3>
            {movie && <Movie movie={movie} />}
        </div>
    );
}

export default Home;