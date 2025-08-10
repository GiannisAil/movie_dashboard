const BASE_URL = "http://localhost:8000/api";

// Function to fetch movies from the backend
export async function getMovies() {
	const response = await fetch(`${BASE_URL}/movies`);
	if (!response.ok) { 
		throw new Error("Failed to fetch movies"); 
	}
	return await response.json();
}