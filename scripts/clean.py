"""
Data Cleaning and Feature Engineering Module
==============================================
Transforms raw TMDB API data into analysis-ready dataframe.

This module handles:
- Extraction of nested JSON fields (genres, cast, crew, production details)
- Data type conversion and validation
- Removal of unrealistic values (zero budgets, invalid ratings)
- Unit conversion (USD to millions, datetime parsing)
- Data quality filtering and imputation
- Final column selection and ordering

Example:
    >>> from scripts.clean import run
    >>> df_raw = pd.read_json("raw_tmdb_movies.json")
    >>> df_clean = run(df_raw)
"""

import numpy as np
import pandas as pd


# ---------- Helper Functions ----------

def extract_collection_name(collection):
    """Extract franchise/collection name from nested collection object.
    
    Args:
        collection: Dict with 'name' key or None.
        
    Returns:
        str: Collection name or NaN if not found.
    """
    if isinstance(collection, dict) and 'name' in collection:
        return collection['name']
    return np.nan


def extract_genres(genres_list):
    """Extract and join genre names from genres list.
    
    Args:
        genres_list: List of genre dicts with 'name' key.
        
    Returns:
        str: Pipe-separated genre names (e.g. 'Action|Sci-Fi|Thriller') or NaN.
    """
    if isinstance(genres_list, list) and len(genres_list) > 0:
        return '|'.join([genre['name'] for genre in genres_list if 'name' in genre])
    return np.nan


def extract_spoken_languages(languages_list):
    """Extract and join spoken language names.
    
    Args:
        languages_list: List of language dicts with 'name' key.
        
    Returns:
        str: Pipe-separated language names or NaN.
    """
    if isinstance(languages_list, list) and len(languages_list) > 0:
        return '|'.join([lang['name'] for lang in languages_list if 'name' in lang])
    return np.nan


def extract_production_countries(countries_list):
    """Extract and join production country names.
    
    Args:
        countries_list: List of country dicts with 'name' key.
        
    Returns:
        str: Pipe-separated country names or NaN.
    """
    if isinstance(countries_list, list) and len(countries_list) > 0:
        return '|'.join([country['name'] for country in countries_list if 'name' in country])
    return np.nan


def extract_production_companies(companies_list):
    """Extract and join production company names.
    
    Args:
        companies_list: List of company dicts with 'name' key.
        
    Returns:
        str: Pipe-separated company names or NaN.
    """
    if isinstance(companies_list, list) and len(companies_list) > 0:
        return '|'.join([company['name'] for company in companies_list if 'name' in company])
    return np.nan


def extract_cast(credits):
    """Extract top 5 cast members from credits dict.
    
    Args:
        credits: Dict with 'cast' key containing list of actor dicts.
        
    Returns:
        str: Pipe-separated actor names (e.g. 'Actor1|Actor2|...') or NaN.
    """
    if isinstance(credits, dict) and 'cast' in credits:
        cast_list = credits['cast'][:5]
        return '|'.join([actor['name'] for actor in cast_list if 'name' in actor])
    return np.nan


def extract_cast_size(credits):
    """Extract total number of cast members.
    
    Args:
        credits: Dict with 'cast' key containing list of actor dicts.
        
    Returns:
        int: Count of cast members or NaN.
    """
    if isinstance(credits, dict) and 'cast' in credits:
        return len(credits['cast'])
    return np.nan


def extract_crew_size(credits):
    """Extract total number of crew members.
    
    Args:
        credits: Dict with 'crew' key containing list of crew dicts.
        
    Returns:
        int: Count of crew members or NaN.
    """
    if isinstance(credits, dict) and 'crew' in credits:
        return len(credits['crew'])
    return np.nan


def extract_director(credits):
    """Extract director name from crew list.
    
    Args:
        credits: Dict with 'crew' key containing list of crew dicts with 'job' field.
        
    Returns:
        str: Director name or 'Unknown' if not found.
    """
    if isinstance(credits, dict) and 'crew' in credits:
        for person in credits['crew']:
            if person.get('job') == 'Director':
                return person.get('name', 'Unknown')
    return 'Unknown'
                


# ---------- Main Cleaning Pipeline ----------

def run(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and transform raw TMDB API data for analysis.
    
    Executes the full data cleaning pipeline:
    1. Drop irrelevant columns
    2. Extract nested JSON fields to flat columns
    3. Convert data types (numeric, datetime)
    4. Replace unrealistic values (0 budget → NaN)
    5. Unit conversion (USD to millions)
    6. Clean empty/invalid text fields
    7. Remove duplicates and incomplete rows
    8. Final column selection and ordering
    
    Args:
        df_raw (pd.DataFrame): Raw dataframe from extract.run() with nested JSON fields.
        
    Returns:
        pd.DataFrame: Clean, analysis-ready dataframe with standardized columns:
                     - Financial: budget_musd, revenue_musd, profit_musd, roi
                     - Ratings: vote_count, vote_average, popularity
                     - Metadata: id, title, genres, director, cast, release_date, etc.
                     
    Note:
        - Output shape: (num_movies, 21 columns)
        - All rows have >= 10 non-null values
        - Only 'Released' status movies included
        
    Example:
        >>> df_clean = run(df_raw)
        >>> print(f"Cleaned shape: {df_clean.shape}")
    """
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
