import numpy as np
import pandas as pd

# ---------- Helper Functions ----------
def extract_collection_name(collection):
    if isinstance(collection, dict) and 'name' in collection:
        return collection['name']
    return np.nan

def extract_genres(genres_list):
    if isinstance(genres_list, list) and len(genres_list) > 0:
        return '|'.join([genre['name'] for genre in genres_list if 'name' in genre])
    return np.nan

def extract_spoken_languages(languages_list):
    if isinstance(languages_list, list) and len(languages_list) > 0:
        return '|'.join([lang['name'] for lang in languages_list if 'name' in lang])
    return np.nan

def extract_production_countries(countries_list):
    if isinstance(countries_list, list) and len(countries_list) > 0:
        return '|'.join([country['name'] for country in countries_list if 'name' in country])
    return np.nan

def extract_production_companies(companies_list):
    if isinstance(companies_list, list) and len(companies_list) > 0:
        return '|'.join([company['name'] for company in companies_list if 'name' in company])
    return np.nan

def extract_cast(credits):
    """Extract top 5 cast members as 'Actor1|Actor2|...' or NaN."""
    if isinstance(credits, dict) and 'cast' in credits:
        cast_list = credits['cast'][:5]
        return '|'.join([actor['name'] for actor in cast_list if 'name' in actor])
    return np.nan

def extract_cast_size(credits):
    if isinstance(credits, dict) and 'cast' in credits:
        return len(credits['cast'])
    return np.nan

def extract_crew_size(credits):
    if isinstance(credits, dict) and 'crew' in credits:
        return len(credits['crew'])
    return np.nan

def extract_director(credits):
    if isinstance(credits, dict) and 'crew' in credits:
        for person in credits['crew']:
            if person.get('job') == 'Director':
                return person.get('name', 'Unknown')
    return 'Unknown'

# ---------- Main Cleaning Pipeline ----------
def run(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    # 1. Drop irrelevant columns
    drop_cols = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
    df = df.drop(columns=[col for col in drop_cols if col in df.columns])
    
    # 2. Extract nested JSON fields to temporary columns
    df['collection_name'] = df['belongs_to_collection'].apply(extract_collection_name)
    df['genre_names'] = df['genres'].apply(extract_genres)
    df['language_codes'] = df['spoken_languages'].apply(extract_spoken_languages)
    df['country_names'] = df['production_countries'].apply(extract_production_countries)
    df['company_names'] = df['production_companies'].apply(extract_production_companies)
    
    # Extract from credits BEFORE dropping it
    df['cast'] = df['credits'].apply(extract_cast)
    df['cast_size'] = df['credits'].apply(extract_cast_size)
    df['crew_size'] = df['credits'].apply(extract_crew_size)
    df['director'] = df['credits'].apply(extract_director)
    
    # 3. Drop raw JSON columns
    json_cols = ['belongs_to_collection', 'genres', 'production_countries',
                 'production_companies', 'spoken_languages', 'credits']
    df = df.drop(columns=[col for col in json_cols if col in df.columns])
    
    # 4. Rename extracted columns to final names
    df = df.rename(columns={
        'genre_names': 'genres',
        'language_codes': 'spoken_languages',
        'country_names': 'production_countries',
        'company_names': 'production_companies'
    })
    
    # 5. Convert numeric columns
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    df['id'] = pd.to_numeric(df['id'], errors='coerce')
    df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')
    df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')
    df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
    df['runtime'] = pd.to_numeric(df['runtime'], errors='coerce')
    
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    # 6. Replace unrealistic values (0 → NaN for budget/revenue/runtime)
    df['budget'] = df['budget'].replace(0, np.nan)
    df['revenue'] = df['revenue'].replace(0, np.nan)
    df['runtime'] = df['runtime'].replace(0, np.nan)
    
    # Convert to millions USD
    df['budget_musd'] = df['budget'] / 1_000_000
    df['revenue_musd'] = df['revenue'] / 1_000_000
    
    # vote_average unreliable when vote_count == 0
    df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan
    
    # Clean empty strings in text fields
    df['overview'] = df['overview'].replace(['', 'No overview found.', 'No Overview'], np.nan)
    df['tagline'] = df['tagline'].replace(['', 'No tagline.'], np.nan)
    
    # 7. Drop duplicates and critical missing values
    df = df.drop_duplicates(subset='id')
    df = df.dropna(subset=['id', 'title'])
    
    # 8. Keep only rows with at least 10 non-null columns
    df = df.dropna(thresh=10)
    
    # 9. Keep only Released movies
    if 'status' in df.columns:
        df = df[df['status'] == 'Released']
        df = df.drop(columns='status')
    
    # 10. Final column ordering
    final_column_order = [
        'id', 'title', 'tagline', 'release_date', 'genres', 'collection_name',
        'original_language', 'budget_musd', 'revenue_musd',
        'production_companies', 'production_countries',
        'vote_count', 'vote_average', 'popularity', 'runtime',
        'overview', 'spoken_languages', 'poster_path',
        'cast', 'cast_size', 'director', 'crew_size'
    ]
    
    # Reindex to match required order (only existing columns)
    existing_cols = [col for col in final_column_order if col in df.columns]
    df = df[existing_cols].copy()
    
    # 11. Reset index
    df = df.reset_index(drop=True)
    
    return df
    df['spoken_languages'] = df['spoken_languages'].apply(extract_spoken_languages)
    df['production_countries'] = df['production_countries'].apply(extract_production_countries)
    df['production_companies'] = df['production_companies'].apply(extract_production_companies)

    df['cast'] = df['credits'].apply(extract_cast)
    df['cast_size'] = df['credits'].apply(extract_cast_size)
    df['crew_size'] = df['credits'].apply(extract_crew_size)
    df['director'] = df['credits'].apply(extract_director)

    json_cols = [
        'belongs_to_collection', 'credits', 'genres',
        'production_countries', 'production_companies', 'spoken_languages'
    ]
    df = df.drop(columns=[c for c in json_cols if c in df.columns])

    num_cols = [
        'budget', 'revenue', 'runtime', 'vote_count',
        'vote_average', 'popularity', 'id'
    ]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    df['budget'] = df['budget'].replace(0, np.nan)
    df['revenue'] = df['revenue'].replace(0, np.nan)
    df['runtime'] = df['runtime'].replace(0, np.nan)

    df['budget_musd'] = df['budget'] / 1_000_000
    df['revenue_musd'] = df['revenue'] / 1_000_000

    df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan

    df['overview'] = df['overview'].replace(['', 'No overview found.'], np.nan)
    df['tagline'] = df['tagline'].replace(['', 'No tagline.'], np.nan)

    df = df.drop_duplicates(subset='id')
    df = df.dropna(subset=['id', 'title'])
    df = df.dropna(thresh=10)

    if 'status' in df.columns:
        df = df[df['status'] == 'Released']
        df = df.drop(columns='status')

    return df.reset_index(drop=True)
