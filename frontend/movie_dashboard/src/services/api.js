const BASE_URL = "http://127.0.0.1:8000/api";

// Function to fetch movies from the backend
export async function getMovies() {
	const response = await fetch(`http://127.0.0.1:8000/api/movies`);
	if (!response.ok) { 
		throw new Error("Failed to fetch movies"); 
	}
	return await response.json();
}

export async function send_csv(formData){
	const res = await fetch("http://127.0.0.1:8000/api/upload_csv", {
		method: "POST",
		body: formData
	})
	if(!res.ok){
		throw new Error("Failed to upload CSV file.");
	}
	const data = await res.json();
	return data; 
}