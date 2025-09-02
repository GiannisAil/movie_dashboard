import { useState, useEffect } from 'react';
import Movie from '../components/Movie';
import UploadCSV from '../components/UploadCSV';
import Stats from '../components/Stats';
import { getMovies } from '../services/api';
import Navbar from '../components/Navbar';
import { Box } from '@chakra-ui/react'

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

    // useEffect(() => {
    //     let ignore = false;

    //     async function fetchMovies(){
    //         const movies = await getMovies();
    //         if(!ignore){
    //             setMovie(movies[0]);
    //         }
    //     }
    //     fetchMovies();
        
    //     return () => {
    //         ignore = true; // Cleanup
    //     };

    // }, []);

    const [stats, setStats] = useState(null)

    return (
        <Box>
            <title>Letterboxd Unboxed</title>
            {/* <Navbar /> */}
            {/* <h1>Movie Dashboard</h1> */}
            {/* <h3>Your Movies:</h3> */}
            {/* {movie && <Movie movie={movie} />} */}
            <UploadCSV statsChanger={setStats} />
            {stats && <Stats stats={stats} />}
        </Box>
    );
}

export default Home;