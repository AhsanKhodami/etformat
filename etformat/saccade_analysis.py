"""
Eye-tracking data saccade amplitude analysis module for etformat package.

This module provides a simple function for calculating average saccade amplitude for each trial
in an eye-tracking events file.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def saccade_amplitude_average(events, output_path=None):
    """
    Calculate average saccade amplitude for each trial in the events file or DataFrame
    and save results to a CSV file.
    
    Parameters:
    -----------
    events (str or DataFrame): Path to events CSV file or pandas DataFrame with events data
    output_path (str, optional): Path to save the output CSV file. If None and events is a path,
                                a path will be generated based on the input file.
    
    Returns:
    --------
    str or DataFrame: Path to the output CSV file with average saccade amplitudes if output_path 
                     is provided or can be generated; otherwise returns the DataFrame with results
    """
    
    try:
        # Check if events is a file path or DataFrame
        if isinstance(events, pd.DataFrame):
            events_df = events
            print("Calculating average saccade amplitudes from DataFrame")
            # If no output_path is provided, we'll return the DataFrame
            if output_path is None:
                return_df = True
            else:
                return_df = False
                output_path = Path(output_path)
        else:
            print(f"Calculating average saccade amplitudes from: {events}")
            # Create output filename if not provided
            events_path = Path(events)
            if output_path is None:
                output_path = events_path.parent / f"{events_path.stem}_average_saccade_amplitude.csv"
                return_df = False
            else:
                output_path = Path(output_path)
                return_df = False
            
            # Load events data
            events_df = pd.read_csv(events)
        
        # Check if trial column exists
        if 'trial' not in events_df.columns:
            print("ERROR: 'trial' column not found in events file!")
            return None
        
        # Get unique trials
        trials = events_df['trial'].dropna().unique()
        print(f"Found {len(trials)} trials in the events file")
        
        # Create results list
        results = []
          # Process each trial
        for trial in trials:
            # Filter for this trial's saccades
            saccades = events_df[(events_df['trial'] == trial) & (events_df['type'] == 'ENDSACC')]
            
            # Calculate average saccade amplitude for this trial
            if not saccades.empty:
                # Calculate pixel distances (Euclidean distance between start and end gaze positions)
                pixel_distances = np.sqrt((saccades['genx'] - saccades['gstx']) ** 2 +
                                         (saccades['geny'] - saccades['gsty']) ** 2)
                
                # Calculate average units-per-degree for each saccade
                avg_units_per_degree = (saccades['supd_x'] + saccades['eupd_x'] +
                                       saccades['supd_y'] + saccades['eupd_y']) / 4
                
                # Calculate saccade amplitude in degrees
                amplitudes_deg = pixel_distances / avg_units_per_degree
                
                # Compute average amplitude across all saccades in this trial
                average_amplitude = amplitudes_deg.mean()
                
                # Add to results
                results.append({
                    'trial': trial,
                    'average': round(average_amplitude, 2)
                })
            else:
                # Still add to results with NaN if no saccades found
                results.append({
                    'trial': trial,
                    'average': np.nan
                })
        
        # Create DataFrame with results
        results_df = pd.DataFrame(results)
        
        # If output_path is provided or we're working with a file path, save to CSV
        if not return_df:
            results_df.to_csv(output_path, index=False)
            print(f"Saved average saccade amplitudes to: {output_path}")
            return str(output_path)
        else:
            # Return the DataFrame directly
            return results_df
            
    except Exception as e:
        print(f"ERROR calculating saccade amplitudes: {e}")
        return None
