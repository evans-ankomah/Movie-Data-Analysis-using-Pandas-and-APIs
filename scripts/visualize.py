"""
Data Visualization Module
==========================
Provides matplotlib-based visualizations for movie analysis.

This module creates:
- Scatter plots for budget vs revenue analysis
- Bar charts for genre and financial metrics
- Multi-panel dashboards for comparative analysis
- Trend analysis over time

Example:
    >>> from scripts.visualize import revenue_vs_budget, franchise_vs_standalone_comparison
    >>> revenue_vs_budget(df)
    >>> franchise_vs_standalone_comparison(df)
"""

import matplotlib.pyplot as plt
import pandas as pd


def revenue_vs_budget(df):
    """Create scatter plot comparing budget vs revenue by franchise status.
    
    Visualizes the relationship between movie budget and revenue, with points
    colored by whether the movie belongs to a franchise or is standalone.
    
    Args:
        df (pd.DataFrame): Movie dataframe with budget_musd, revenue_musd, collection_name columns.
        
    Returns:
        None. Displays matplotlib figure.
        
    Examples:
        >>> revenue_vs_budget(df_final)
    """
    df = df.copy()
    df['Movie Type'] = df['collection_name'].notna().map({True: 'Franchise', False: 'Standalone'})
    
    plt.figure(figsize=(10, 6))
    colors = {'Franchise': 'orange', 'Standalone': 'blue'}
    
    for movie_type, group in df.groupby('Movie Type'):
        plt.scatter(group['budget_musd'], group['revenue_musd'],
                    label=movie_type, alpha=0.7, s=80, c=colors[movie_type],
                    edgecolors='black', linewidth=0.5)
    
    plt.xlabel('Budget (Million USD)', fontsize=12)
    plt.ylabel('Revenue (Million USD)', fontsize=12)
    plt.title('Revenue vs Budget (Colored by Franchise vs Standalone)', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Movie Type', fontsize=10)
    plt.tight_layout()
    plt.show()


def roi_by_genre(df):
    """Create bar chart showing average ROI by genre.
    
    Displays average Return on Investment for the top 6 genres, limited to
    movies with budget >= $10M for meaningful ROI analysis.
    
    Args:
        df (pd.DataFrame): Movie dataframe with genres, budget_musd, roi columns.
        
    Returns:
        None. Displays matplotlib figure.
        
    Examples:
        >>> roi_by_genre(df_final)
    """
    df = df.copy()
    
    # Get primary genre
    df['primary_genre'] = df['genres'].str.split('|').str[0]
    
    # Filter for valid ROI data
    df_roi = df[(df['budget_musd'] >= 10) & (df['roi'].notna())]
    
    # Get top 6 genres
    top_genres = df_roi['primary_genre'].value_counts().head(6).index
    df_genre = df_roi[df_roi['primary_genre'].isin(top_genres)]
    
    # Calculate mean ROI per genre
    genre_roi = df_genre.groupby('primary_genre')['roi'].mean().sort_values()
    
    plt.figure(figsize=(10, 6))
    plt.barh(genre_roi.index, genre_roi.values, color='steelblue', edgecolor='black')
    plt.xlabel('Average ROI', fontsize=12)
    plt.ylabel('Genre', fontsize=12)
    plt.title('ROI Distribution by Genre (Budget ≥ $10M)', fontweight='bold', fontsize=14)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()


def popularity_vs_rating(df):
    """Create scatter plot comparing popularity vs rating by franchise status.
    
    Shows the relationship between user ratings (vote_average) and popularity scores,
    colored by franchise status. Only includes movies with >= 10 votes for credibility.
    
    Args:
        df (pd.DataFrame): Movie dataframe with vote_average, popularity, vote_count, collection_name.
        
    Returns:
        None. Displays matplotlib figure.
        
    Examples:
        >>> popularity_vs_rating(df_final)
    """
    df = df.copy()
    
    # Filter movies with at least 10 votes
    df_valid = df[df['vote_count'] >= 10].copy()
    df_valid['Movie Type'] = df_valid['collection_name'].notna().map({True: 'Franchise', False: 'Standalone'})
    
    plt.figure(figsize=(10, 6))
    colors = {'Franchise': 'orange', 'Standalone': 'blue'}
    
    for movie_type, group in df_valid.groupby('Movie Type'):
        plt.scatter(group['vote_average'], group['popularity'],
                    label=movie_type, alpha=0.7, s=100, c=colors[movie_type],
                    edgecolors='black', linewidth=0.5)
    
    plt.xlabel('Vote Average (Rating)', fontsize=12)
    plt.ylabel('Popularity Score', fontsize=12)
    plt.title('Popularity vs Rating\n(Colored by Franchise vs Standalone)', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Movie Type', fontsize=10)
    plt.tight_layout()
    plt.show()


def yearly_trends(df):
    """Create dual chart showing yearly box office trends.
    
    Left panel: Line chart of total revenue by year.
    Right panel: Bar chart of number of movies released per year.
    
    Args:
        df (pd.DataFrame): Movie dataframe with release_date, revenue_musd columns.
        
    Returns:
        None. Displays matplotlib figure with subplots.
        
    Examples:
        >>> yearly_trends(df_final)
    """
    df = df.copy()
    df['release_year'] = pd.to_datetime(df['release_date']).dt.year
    
    # Group by year
    yearly = df.groupby('release_year').agg({
        'revenue_musd': 'sum',
        'budget_musd': 'mean',
        'title': 'count'
    }).reset_index()
    
    yearly.columns = ['year', 'total_revenue', 'mean_budget', 'movie_count']
    
    # Create 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Total Revenue per Year
    ax1.plot(yearly['year'], yearly['total_revenue'], marker='o', linewidth=2, markersize=8, color='steelblue')
    ax1.set_xlabel('Year', fontsize=11)
    ax1.set_ylabel('Total Revenue (Million USD)', fontsize=11)
    ax1.set_title('Total Box Office Revenue by Year', fontweight='bold', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Number of Movies per Year
    ax2.bar(yearly['year'], yearly['movie_count'], color='coral', edgecolor='black')
    ax2.set_xlabel('Year', fontsize=11)
    ax2.set_ylabel('Number of Movies', fontsize=11)
    ax2.set_title('Movies Released per Year', fontweight='bold', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def franchise_vs_standalone_comparison(df):
    """Create 4-panel dashboard comparing franchise vs standalone metrics.
    
    Displays side-by-side bar charts for:
    - Average Revenue
    - Average Budget
    - Average Popularity
    - Average Rating
    
    Args:
        df (pd.DataFrame): Movie dataframe with collection_name, revenue_musd, budget_musd, etc.
        
    Returns:
        None. Displays matplotlib figure with 2x2 subplots.
        
    Examples:
        >>> franchise_vs_standalone_comparison(df_final)
    """
    df = df.copy()
    df['is_franchise'] = df['collection_name'].notna()
    
    # Calculate comparison metrics
    comparison = df.groupby('is_franchise').agg({
        'revenue_musd': 'mean',
        'budget_musd': 'mean',
        'popularity': 'mean',
        'vote_average': 'mean',
        'title': 'count'
    }).reset_index()
    
    comparison['type'] = comparison['is_franchise'].map({True: 'Franchise', False: 'Standalone'})
    
    # Create 2x2 subplot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Mean Revenue
    axes[0, 0].bar(comparison['type'], comparison['revenue_musd'], color='steelblue', edgecolor='black')
    axes[0, 0].set_ylabel('Mean Revenue (M USD)', fontsize=11)
    axes[0, 0].set_title('Average Revenue', fontweight='bold', fontsize=12)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Plot 2: Mean Budget
    axes[0, 1].bar(comparison['type'], comparison['budget_musd'], color='coral', edgecolor='black')
    axes[0, 1].set_ylabel('Mean Budget (M USD)', fontsize=11)
    axes[0, 1].set_title('Average Budget', fontweight='bold', fontsize=12)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Plot 3: Mean Popularity
    axes[1, 0].bar(comparison['type'], comparison['popularity'], color='lightgreen', edgecolor='black')
    axes[1, 0].set_ylabel('Mean Popularity', fontsize=11)
    axes[1, 0].set_title('Average Popularity', fontweight='bold', fontsize=12)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Plot 4: Mean Rating
    axes[1, 1].bar(comparison['type'], comparison['vote_average'], color='gold', edgecolor='black')
    axes[1, 1].set_ylabel('Mean Rating', fontsize=11)
    axes[1, 1].set_title('Average Rating', fontweight='bold', fontsize=12)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    df = df.copy()
    df['Movie Type'] = df['collection_name'].notna().map({True: 'Franchise', False: 'Standalone'})
    
    plt.figure(figsize=(10, 6))
    colors = {'Franchise': 'orange', 'Standalone': 'blue'}
    
    for movie_type, group in df.groupby('Movie Type'):
        plt.scatter(group['budget_musd'], group['revenue_musd'],
                    label=movie_type, alpha=0.7, s=80, c=colors[movie_type],
                    edgecolors='black', linewidth=0.5)
    
    plt.xlabel('Budget (Million USD)', fontsize=12)
    plt.ylabel('Revenue (Million USD)', fontsize=12)
    plt.title('Revenue vs Budget (Colored by Franchise vs Standalone)', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Movie Type', fontsize=10)
    plt.tight_layout()
    plt.show()

def roi_by_genre(df):
    """Bar chart showing average ROI by genre (for budget >= $10M)."""
    df = df.copy()
    
    # Get primary genre
    df['primary_genre'] = df['genres'].str.split('|').str[0]
    
    # Filter for valid ROI data
    df_roi = df[(df['budget_musd'] >= 10) & (df['roi'].notna())]
    
    # Get top 6 genres
    top_genres = df_roi['primary_genre'].value_counts().head(6).index
    df_genre = df_roi[df_roi['primary_genre'].isin(top_genres)]
    
    # Calculate mean ROI per genre
    genre_roi = df_genre.groupby('primary_genre')['roi'].mean().sort_values()
    
    plt.figure(figsize=(10, 6))
    plt.barh(genre_roi.index, genre_roi.values, color='steelblue', edgecolor='black')
    plt.xlabel('Average ROI', fontsize=12)
    plt.ylabel('Genre', fontsize=12)
    plt.title('ROI Distribution by Genre (Budget ≥ $10M)', fontweight='bold', fontsize=14)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

def popularity_vs_rating(df):
    """Scatter plot of popularity vs rating, colored by franchise status."""
    df = df.copy()
    
    # Filter movies with at least 10 votes
    df_valid = df[df['vote_count'] >= 10].copy()
    df_valid['Movie Type'] = df_valid['collection_name'].notna().map({True: 'Franchise', False: 'Standalone'})
    
    plt.figure(figsize=(10, 6))
    colors = {'Franchise': 'orange', 'Standalone': 'blue'}
    
    for movie_type, group in df_valid.groupby('Movie Type'):
        plt.scatter(group['vote_average'], group['popularity'],
                    label=movie_type, alpha=0.7, s=100, c=colors[movie_type],
                    edgecolors='black', linewidth=0.5)
    
    plt.xlabel('Vote Average (Rating)', fontsize=12)
    plt.ylabel('Popularity Score', fontsize=12)
    plt.title('Popularity vs Rating\n(Colored by Franchise vs Standalone)', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(title='Movie Type', fontsize=10)
    plt.tight_layout()
    plt.show()

def yearly_trends(df):
    """Line and bar chart showing yearly box office trends."""
    df = df.copy()
    df['release_year'] = pd.to_datetime(df['release_date']).dt.year
    
    # Group by year
    yearly = df.groupby('release_year').agg({
        'revenue_musd': 'sum',
        'budget_musd': 'mean',
        'title': 'count'
    }).reset_index()
    
    yearly.columns = ['year', 'total_revenue', 'mean_budget', 'movie_count']
    
    # Create 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Total Revenue per Year
    ax1.plot(yearly['year'], yearly['total_revenue'], marker='o', linewidth=2, markersize=8, color='steelblue')
    ax1.set_xlabel('Year', fontsize=11)
    ax1.set_ylabel('Total Revenue (Million USD)', fontsize=11)
    ax1.set_title('Total Box Office Revenue by Year', fontweight='bold', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Number of Movies per Year
    ax2.bar(yearly['year'], yearly['movie_count'], color='coral', edgecolor='black')
    ax2.set_xlabel('Year', fontsize=11)
    ax2.set_ylabel('Number of Movies', fontsize=11)
    ax2.set_title('Movies Released per Year', fontweight='bold', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def franchise_vs_standalone_comparison(df):
    """4-panel subplot comparing franchise vs standalone metrics."""
    df = df.copy()
    df['is_franchise'] = df['collection_name'].notna()
    
    # Calculate comparison metrics
    comparison = df.groupby('is_franchise').agg({
        'revenue_musd': 'mean',
        'budget_musd': 'mean',
        'popularity': 'mean',
        'vote_average': 'mean',
        'title': 'count'
    }).reset_index()
    
    comparison['type'] = comparison['is_franchise'].map({True: 'Franchise', False: 'Standalone'})
    
    # Create 2x2 subplot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Mean Revenue
    axes[0, 0].bar(comparison['type'], comparison['revenue_musd'], color='steelblue', edgecolor='black')
    axes[0, 0].set_ylabel('Mean Revenue (M USD)', fontsize=11)
    axes[0, 0].set_title('Average Revenue', fontweight='bold', fontsize=12)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Plot 2: Mean Budget
    axes[0, 1].bar(comparison['type'], comparison['budget_musd'], color='coral', edgecolor='black')
    axes[0, 1].set_ylabel('Mean Budget (M USD)', fontsize=11)
    axes[0, 1].set_title('Average Budget', fontweight='bold', fontsize=12)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Plot 3: Mean Popularity
    axes[1, 0].bar(comparison['type'], comparison['popularity'], color='lightgreen', edgecolor='black')
    axes[1, 0].set_ylabel('Mean Popularity', fontsize=11)
    axes[1, 0].set_title('Average Popularity', fontweight='bold', fontsize=12)
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Plot 4: Mean Rating
    axes[1, 1].bar(comparison['type'], comparison['vote_average'], color='gold', edgecolor='black')
    axes[1, 1].set_ylabel('Mean Rating', fontsize=11)
    axes[1, 1].set_title('Average Rating', fontweight='bold', fontsize=12)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

