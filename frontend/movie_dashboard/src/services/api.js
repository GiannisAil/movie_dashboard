const BASE_URL = "http://127.0.0.1:8000/api";

// Function to fetch movies from the backend
export async function getMovies() {
	const response = await fetch(`http://127.0.0.1:8000/api/movies`);
	if (!response.ok) { 
		throw new Error("Failed to fetch movies"); 
	}
	return await response.json();
}