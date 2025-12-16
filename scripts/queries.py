"""
Advanced Query Module
=====================
Provides specialized filtering and analysis functions for movie data.

This module includes:
- Actor/director-based filtering with ratings
- Franchise analysis and comparison
- Director performance metrics
- Complex multi-criteria queries

Example:
    >>> from scripts.queries import bruce_willis_scifi_action, franchise_analysis
    >>> bruce_movies = bruce_willis_scifi_action(df)
    >>> comparison = franchise_analysis(df)
"""

import pandas as pd


def bruce_willis_scifi_action(df):
    """Filter for Science Fiction Action movies starring Bruce Willis.
    
    Returns all movies where Bruce Willis appears in the cast AND the movie
    contains both 'Science Fiction' and 'Action' in its genres.
    Results are sorted by rating (highest to lowest).
    
    Args:
        df (pd.DataFrame): Movie dataframe with 'genres', 'cast' columns.
        
    Returns:
        pd.DataFrame: Subset of movies with columns: title, vote_average, vote_count, genres, cast.
 
    """
    result = df[
        (df['genres'].str.contains('Science Fiction', case=False, na=False)) &
        (df['genres'].str.contains('Action', case=False, na=False)) &
        (df['cast'].str.contains('Bruce Willis', case=False, na=False))
    ].copy()
    
    # Sort by rating (highest to lowest)
    result = result.sort_values('vote_average', ascending=False)
    return result[['title', 'vote_average', 'vote_count', 'genres', 'cast']]


def uma_thurman_tarantino(df):
    """Filter for movies starring Uma Thurman, directed by Quentin Tarantino.
    
    Returns all movies featuring Uma Thurman in the cast that were directed
    by Quentin Tarantino. Results are sorted by runtime (shortest to longest).
    
    Args:
        df (pd.DataFrame): Movie dataframe with 'cast' and 'director' columns.
        
    Returns:
        pd.DataFrame: Subset of movies with columns: title, runtime, director, cast, release_date.
        
    """
    result = df[
        (df['cast'].str.contains('Uma Thurman', case=False, na=False)) &
        (df['director'].str.contains('Quentin Tarantino', case=False, na=False))
    ].copy()
    
    # Sort by runtime (shortest to longest)
    result = result.sort_values('runtime', ascending=True)
    return result[['title', 'runtime', 'director', 'cast', 'release_date']]


def franchise_analysis(df):
    """Compare franchise vs standalone movie performance.
    
    Calculates aggregate metrics for franchise films (movies with collection_name)
    vs standalone films. Returns a comparison dataframe showing mean/median values
    for key performance metrics.
    
    Args:
        df (pd.DataFrame): Movie dataframe with collection_name, revenue_musd, budget_musd, etc.
        
    Returns:
        pd.DataFrame: Comparison table with metrics: Revenue, ROI, Budget, Popularity, Rating.
                     Columns: Metric, Franchise Movies, Standalone Movies, Difference.

    """
    df = df.copy()
    df['is_franchise'] = df['collection_name'].notna()
    
    franchise_movies = df[df['is_franchise'] == True]
    standalone_movies = df[df['is_franchise'] == False]
    
    comparison_data = {
        'Metric': ['Mean Revenue (M USD)', 'Median ROI', 'Mean Budget (M USD)', 
                   'Mean Popularity', 'Mean Rating'],
        'Franchise Movies': [
            franchise_movies['revenue_musd'].mean(),
            franchise_movies['roi'].median(),
            franchise_movies['budget_musd'].mean(),
            franchise_movies['popularity'].mean(),
            franchise_movies['vote_average'].mean()
        ],
        'Standalone Movies': [
            standalone_movies['revenue_musd'].mean(),
            standalone_movies['roi'].median(),
            standalone_movies['budget_musd'].mean(),
            standalone_movies['popularity'].mean(),
            standalone_movies['vote_average'].mean()
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df['Difference'] = comparison_df['Franchise Movies'] - comparison_df['Standalone Movies']
    
    return comparison_df


def top_franchises(df):
    """Get top franchises ranked by total revenue.
    
    Groups movies by collection_name (franchise) and aggregates financial &
    rating metrics. Returns franchises sorted by total revenue (highest first).
    
    Args:
        df (pd.DataFrame): Movie dataframe with collection_name, budget_musd, revenue_musd.
        
    Returns:
        pd.DataFrame: Franchise statistics with columns: num_movies, total_budget, mean_budget,
                     total_revenue, mean_revenue, mean_rating. Sorted by total_revenue descending.
                     
    Examples:
        >>> top_franchises_df = top_franchises(df)
        >>> print(top_franchises_df.head(5))
    """
    franchise_only = df[df['collection_name'].notna()].copy()
    
    if len(franchise_only) == 0:
        return pd.DataFrame()
    
    franchise_stats = franchise_only.groupby('collection_name').agg({
        'id': 'count',
        'budget_musd': ['sum', 'mean'],
        'revenue_musd': ['sum', 'mean'],
        'vote_average': 'mean'
    }).round(2)
    
    # Flatten column names
    franchise_stats.columns = ['num_movies', 'total_budget', 'mean_budget',
                                'total_revenue', 'mean_revenue', 'mean_rating']
    
    # Sort by total revenue
    franchise_stats = franchise_stats.sort_values('total_revenue', ascending=False)
    
    return franchise_stats


def top_directors(df, min_movies=1):
    """Get top directors ranked by total revenue.
    
    Groups movies by director and aggregates revenue and rating metrics.
    Returns only directors meeting the minimum movie threshold, sorted
    by total revenue (highest first).
    
    Args:
        df (pd.DataFrame): Movie dataframe with director and revenue_musd columns.
        min_movies (int, optional): Minimum number of movies to qualify. Defaults to 1.
        
    Returns:
        pd.DataFrame: Director statistics with columns: num_movies, total_revenue, mean_rating.
                     Sorted by total_revenue descending.
                     
    Examples:
        >>> top_10_directors = top_directors(df, min_movies=1).head(10)
        >>> prolific = top_directors(df, min_movies=2)
    """
    directors_df = df[df['director'] != 'Unknown'].copy()
    
    if len(directors_df) == 0:
        return pd.DataFrame()
    
    director_stats = directors_df.groupby('director').agg({
        'id': 'count',
        'revenue_musd': 'sum',
        'vote_average': 'mean'
    }).round(2)
    
    director_stats.columns = ['num_movies', 'total_revenue', 'mean_rating']
    director_stats = director_stats[director_stats['num_movies'] >= min_movies]
    director_stats = director_stats.sort_values('total_revenue', ascending=False)
    
    return director_stats
    result = df[
        (df['genres'].str.contains('Science Fiction', case=False, na=False)) &
        (df['genres'].str.contains('Action', case=False, na=False)) &
        (df['cast'].str.contains('Bruce Willis', case=False, na=False))
    ].copy()
    
    # Sort by rating (highest to lowest)
    result = result.sort_values('vote_average', ascending=False)
    return result[['title', 'vote_average', 'vote_count', 'genres', 'cast']]

def uma_thurman_tarantino(df):
    """Filter for movies starring Uma Thurman, directed by Quentin Tarantino."""
    result = df[
        (df['cast'].str.contains('Uma Thurman', case=False, na=False)) &
        (df['director'].str.contains('Quentin Tarantino', case=False, na=False))
    ].copy()
    
    # Sort by runtime (shortest to longest)
    result = result.sort_values('runtime', ascending=True)
    return result[['title', 'runtime', 'director', 'cast', 'release_date']]

def franchise_analysis(df):
    """Compare franchise vs standalone movie performance."""
    df = df.copy()
    df['is_franchise'] = df['collection_name'].notna()
    
    franchise_movies = df[df['is_franchise'] == True]
    standalone_movies = df[df['is_franchise'] == False]
    
    comparison_data = {
        'Metric': ['Mean Revenue (M USD)', 'Median ROI', 'Mean Budget (M USD)', 
                   'Mean Popularity', 'Mean Rating'],
        'Franchise Movies': [
            franchise_movies['revenue_musd'].mean(),
            franchise_movies['roi'].median(),
            franchise_movies['budget_musd'].mean(),
            franchise_movies['popularity'].mean(),
            franchise_movies['vote_average'].mean()
        ],
        'Standalone Movies': [
            standalone_movies['revenue_musd'].mean(),
            standalone_movies['roi'].median(),
            standalone_movies['budget_musd'].mean(),
            standalone_movies['popularity'].mean(),
            standalone_movies['vote_average'].mean()
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df['Difference'] = comparison_df['Franchise Movies'] - comparison_df['Standalone Movies']
    
    return comparison_df

def top_franchises(df):
    """Get top franchises ranked by total revenue."""
    franchise_only = df[df['collection_name'].notna()].copy()
    
    if len(franchise_only) == 0:
        return pd.DataFrame()
    
    franchise_stats = franchise_only.groupby('collection_name').agg({
        'id': 'count',
        'budget_musd': ['sum', 'mean'],
        'revenue_musd': ['sum', 'mean'],
        'vote_average': 'mean'
    }).round(2)
    
    # Flatten column names
    franchise_stats.columns = ['num_movies', 'total_budget', 'mean_budget',
                                'total_revenue', 'mean_revenue', 'mean_rating']
    
    # Sort by total revenue
    franchise_stats = franchise_stats.sort_values('total_revenue', ascending=False)
    
    return franchise_stats

def top_directors(df, min_movies=1):
    """Get top directors ranked by total revenue."""
    directors_df = df[df['director'] != 'Unknown'].copy()
    
    if len(directors_df) == 0:
        return pd.DataFrame()
    
    director_stats = directors_df.groupby('director').agg({
        'id': 'count',
        'revenue_musd': 'sum',
        'vote_average': 'mean'
    }).round(2)
    
    director_stats.columns = ['num_movies', 'total_revenue', 'mean_rating']
    director_stats = director_stats[director_stats['num_movies'] >= min_movies]
    director_stats = director_stats.sort_values('total_revenue', ascending=False)
    
    return director_stats
