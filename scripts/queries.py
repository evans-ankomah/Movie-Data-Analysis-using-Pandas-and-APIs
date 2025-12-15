import pandas as pd

def bruce_willis_scifi_action(df):
    """Filter for Science Fiction Action movies starring Bruce Willis."""
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
