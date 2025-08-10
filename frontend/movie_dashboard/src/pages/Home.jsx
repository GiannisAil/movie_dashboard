import Movie from '../components/Movie';

function Home(){
    // movie data for testing
    let movie = {
        "id": 1,
        "title": "The Matrix",
        "year": 1999,
        "rating": 9,
        "date_watched": "2024-02-14",
        "genre": [
          "Action",
          "Thriller"
        ],
        "director": "Wachowski"
    }

    return (
        <div>
            <h1>Movie Dashboard</h1>
            <h4>Movie List.</h4>
            <h4>Add a movie</h4>
            <h5>Movie test</h5>
            <Movie movie={movie} />
        </div>
    );
}

export default Home;