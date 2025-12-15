import time
import requests
import pandas as pd
from config import API_KEY, BASE_URL, MOVIE_IDS

def fetch_movie(movie_id: int) -> dict:
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
    raw_movies_data = []

    for mid in MOVIE_IDS:
        movie = fetch_movie(mid)
        if movie:
            raw_movies_data.append(movie)
        time.sleep(0.22)

    df_raw = pd.DataFrame(raw_movies_data)
    df_raw.to_json("raw_tmdb_movies.json", orient="records", indent=2)

    return df_raw
