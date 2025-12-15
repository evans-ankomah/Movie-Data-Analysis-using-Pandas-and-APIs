import pandas as pd
import numpy as np

def add_kpis(df):
    """Add calculated metrics: profit and ROI."""
    df = df.copy()
    df['profit_musd'] = df['revenue_musd'] - df['budget_musd']
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    return df

def get_top_movies(df, metric, top_n=5, ascending=False, filter_condition=None, display_cols=None):
   
    if display_cols is None:
        display_cols = ['title', metric, 'release_date', 'genres']
    
    # Validation: metric must exist
    if metric not in df.columns:
        raise KeyError(f"Metric column '{metric}' not found. Available columns: {list(df.columns)}")
    
    # Apply filter if provided
    if filter_condition is not None:
        df_filtered = df[filter_condition].copy()
    else:
        df_filtered = df.copy()
    
    # Coerce metric to numeric if necessary
    if not pd.api.types.is_numeric_dtype(df_filtered[metric]):
        df_filtered[metric] = pd.to_numeric(df_filtered[metric], errors='coerce')
    
    # Remove rows where metric is NaN
    df_filtered = df_filtered.dropna(subset=[metric])
    
    # Return empty DataFrame if no valid data
    if df_filtered.empty:
        existing_cols = [c for c in display_cols if c in df.columns]
        return pd.DataFrame(columns=existing_cols)
    
    # Select top/bottom N
    result = df_filtered.nlargest(top_n, metric) if not ascending else df_filtered.nsmallest(top_n, metric)
    
    # Only return columns that exist
    cols_to_show = [c for c in display_cols if c in result.columns]
    if not cols_to_show:
        cols_to_show = result.columns.tolist()[:4]
    
    return result[cols_to_show]
