// React component to display a single movie

// api response:
// [
//   {
//     "id": 1,
//     "title": "The Matrix",
//     "year": 1999,
//     "rating": 9,
//     "date_watched": "2024-02-14",
//     "genre": [
//       "Action",
//       "Thriller"
//     ],
//     "director": "Wachowski"
//   },
//   {
//     "id": 2,
//     "title": "La La Land",
//     "year": 2016,
//     "rating": 8,
//     "date_watched": "2024-03-02",
//     "genre": [
//       "Musical"
//     ],
//     "director": "Chazelle"
//   }
// ]

// Movie(id=1, title="The Matrix", year=1999, rating=9, date_watched="2024-02-14", genre=["Action", "Thriller"], director="Wachowski"),

function Movie({movie}) {
    return (
        <div className="movie" style={{ border: '1px solid #ccc', padding: '10px', margin: '10px' }}>
            <h2>{movie.title} ({movie.year})</h2>
            <p>Rating: {movie.rating}</p>
            <p>Date Watched: {movie.date_watched}</p>
            <p>Genre: {movie.genre.join(", ")}</p>
            <p>Director: {movie.director}</p>
        </div>
    );
}

export default Movie;