"""
Eye-tracking data cleaning module for etformat package.

This module provides a function for cleaning eye-tracking data by removing rows with NaN trials
and removing empty or zero-filled columns.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def clean(samples, events, verbose=True, copy=False):
    """
    Clean eye-tracking data by:
    1. Removing rows where 'trial' is NaN
    2. Removing columns that are entirely NaN or 0
    
    Parameters:
    -----------
    samples (str or DataFrame): Path to samples CSV file or pandas DataFrame with samples data
    events (str or DataFrame): Path to events CSV file or pandas DataFrame with events data
    verbose (bool): Print cleaning statistics (default: True)
    copy (bool): If True, saves to new files instead of overwriting originals when path is provided (default: False)
    
    Returns:
    --------
    tuple: When file paths are provided and copy=False: (samples_path, events_path) - Paths to the cleaned files
           When file paths are provided and copy=True: (new_samples_path, new_events_path) - Paths to the new cleaned files
           When DataFrames are provided: (samples_df, events_df) - Cleaned DataFrames
    """
    
    print(f"🧹 Starting data cleaning for eye-tracking data")
    
    # Determine if inputs are paths or DataFrames
    samples_is_path = not isinstance(samples, pd.DataFrame)
    events_is_path = not isinstance(events, pd.DataFrame)
    
    # Set output variables
    samples_output_path = None
    events_output_path = None
    
    # Handle file paths and prepare output paths
    if samples_is_path:
        print(f"   📊 Samples: {samples}")
        samples_output_path = samples
        
        if copy:
            samples_path = Path(samples)
            samples_output_path = samples_path.parent / f"{samples_path.stem}_cleaned{samples_path.suffix}"
            print(f"   📝 Creating cleaned copy: {samples_output_path}")
    else:
        print(f"   📊 Samples: DataFrame with shape {samples.shape}")
    
    if events_is_path:
        print(f"   📊 Events: {events}")
        events_output_path = events
        
        if copy:
            events_path = Path(events)
            events_output_path = events_path.parent / f"{events_path.stem}_cleaned{events_path.suffix}"
            print(f"   📝 Creating cleaned copy: {events_output_path}")
    else:
        print(f"   📊 Events: DataFrame with shape {events.shape}")
    
    print("="*60)    # Clean samples data
    print("\n🔍 Processing SAMPLES data...")
    try:
        # Load samples data if it's a file path
        if samples_is_path:
            samples_df = pd.read_csv(samples)
        else:
            # Make a copy of the DataFrame to avoid modifying the original
            samples_df = samples.copy()
            
        original_samples_shape = samples_df.shape
        original_columns = len(samples_df.columns)
        
        if verbose:
            print(f"   Original samples shape: {original_samples_shape}")
            print(f"   Columns: {original_columns}")
        
        # Step 1: Remove rows where 'trial' is NaN
        if 'trial' in samples_df.columns:
            nan_trials = samples_df['trial'].isna().sum()
            samples_df = samples_df.dropna(subset=['trial'])
            if verbose and nan_trials > 0:
                print(f"   ❌ Removed {nan_trials} rows with NaN trials")
        else:
            print("   ⚠️  Warning: 'trial' column not found in samples!")
        
        # Step 2: Identify and remove columns that are entirely NaN or 0
        cols_to_remove = []
        
        for col in samples_df.columns:
            # Check if column is entirely NaN
            if samples_df[col].isna().all():
                cols_to_remove.append((col, "all_nan"))
            # Check if column is entirely 0 (excluding NaN)
            elif samples_df[col].dropna().eq(0).all() and not samples_df[col].dropna().empty:
                cols_to_remove.append((col, "all_zero"))
        
        # Remove identified columns
        if cols_to_remove:
            cols_names = [col[0] for col in cols_to_remove]
            samples_df = samples_df.drop(columns=cols_names)
            if verbose:
                print(f"   ❌ Removed {len(cols_to_remove)} columns:")
                for col, reason in cols_to_remove:
                    print(f"      • {col} ({reason})")
        
        # Save cleaned samples if it was a file path
        if samples_is_path:
            samples_df.to_csv(samples_output_path, index=False)
            cleaned_samples_shape = samples_df.shape
            print(f"   ✅ Samples cleaned: {original_samples_shape} → {cleaned_samples_shape}")
            print(f"   💾 Saved to: {samples_output_path}")
        else:
            cleaned_samples_shape = samples_df.shape
            print(f"   ✅ Samples cleaned: {original_samples_shape} → {cleaned_samples_shape}")
        
    except Exception as e:
        print(f"   ❌ ERROR processing samples: {e}")
        return None, None
    
    # Clean events data
    print("\n🔍 Processing EVENTS data...")
    try:
        # Load events data if it's a file path
        if events_is_path:
            events_df = pd.read_csv(events)
        else:
            # Make a copy of the DataFrame to avoid modifying the original
            events_df = events.copy()
            
        original_events_shape = events_df.shape
        original_columns = len(events_df.columns)
        
        if verbose:
            print(f"   Original events shape: {original_events_shape}")
            print(f"   Columns: {original_columns}")
        
        # Step 1: Remove rows where 'trial' is NaN
        if 'trial' in events_df.columns:
            nan_trials = events_df['trial'].isna().sum()
            events_df = events_df.dropna(subset=['trial'])
            if verbose and nan_trials > 0:
                print(f"   ❌ Removed {nan_trials} rows with NaN trials")
        else:
            print("   ⚠️  Warning: 'trial' column not found in events!")
        
        # Step 2: Identify and remove columns that are entirely NaN or 0
        cols_to_remove = []
        
        for col in events_df.columns:
            # Check if column is entirely NaN
            if events_df[col].isna().all():
                cols_to_remove.append((col, "all_nan"))
            # Check if column is entirely 0 (excluding NaN and string columns)
            elif events_df[col].dtype in ['int64', 'float64']:
                if events_df[col].dropna().eq(0).all() and not events_df[col].dropna().empty:
                    cols_to_remove.append((col, "all_zero"))
        
        # Remove identified columns
        if cols_to_remove:
            cols_names = [col[0] for col in cols_to_remove]
            events_df = events_df.drop(columns=cols_names)
            if verbose:
                print(f"   ❌ Removed {len(cols_to_remove)} columns:")
                for col, reason in cols_to_remove:
                    print(f"      • {col} ({reason})")
        
        # Save cleaned events if it was a file path
        if events_is_path:
            events_df.to_csv(events_output_path, index=False)
            cleaned_events_shape = events_df.shape
            print(f"   ✅ Events cleaned: {original_events_shape} → {cleaned_events_shape}")
            print(f"   💾 Saved to: {events_output_path}")
        else:
            cleaned_events_shape = events_df.shape
            print(f"   ✅ Events cleaned: {original_events_shape} → {cleaned_events_shape}")
        
    except Exception as e:
        print(f"   ❌ ERROR processing events: {e}")
        if samples_is_path:
            return samples_output_path, None
        else:
            return samples_df, None
    
    print("="*60)
    print("🎉 Cleaning completed!")
    
    # Return appropriate values based on input types
    if samples_is_path and events_is_path:
        return samples_output_path, events_output_path
    else:
        return samples_df, events_df
