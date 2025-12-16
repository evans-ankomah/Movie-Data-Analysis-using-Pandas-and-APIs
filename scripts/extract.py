"""
Data Extraction Module
======================
Fetches movie data from The Movie Database (TMDB) API.

This module handles:
- Individual movie data retrieval with credits
- Batch processing with rate limiting
- Error handling for API failures
- JSON persistence

Example:
   
"""

import time
import requests
import pandas as pd
from config import API_KEY, BASE_URL, MOVIE_IDS


def fetch_movie(movie_id: int) -> dict:
    """Fetch single movie data from TMDB API.
    
    Retrieves movie details including credits (cast & crew) in a single request
    using the append_to_response parameter.
    
    Args:
        movie_id: The unique TMDB movie identifier (integer).
        
    Returns:
        dict: Raw JSON response containing movie data, or None if not found.
        
    Raises:
        Exception: If API returns an error code (except 404).
        
    """
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "append_to_response": "credits"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def run() -> pd.DataFrame:
    """Fetch all movies from TMDB API and save to JSON.
    
    Iterates through MOVIE_IDS from config.py, fetches each movie's data,
    and applies polite rate limiting (0.22s delay = ~4-5 requests/sec).
    Successfully fetched data is saved to raw_tmdb_movies.json.
    
    Returns:
        pd.DataFrame: DataFrame containing raw API response data for all movies.
                     Columns include: id, title, budget, revenue, genres, credits, etc.
                     
    Note:
        - Failed requests (404, errors) are silently skipped
        - Rate limiting prevents API throttling
        - Output saved to raw_tmdb_movies.json
    """
    raw_movies_data = []

    for mid in MOVIE_IDS:
        movie = fetch_movie(mid)
        if movie:
            raw_movies_data.append(movie)
        time.sleep(0.22)

    df_raw = pd.DataFrame(raw_movies_data)
   

    return df_raw
