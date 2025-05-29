"""
Eye-tracking data report generation module for etformat package.

This module provides functions for generating comprehensive trial reports from eye-tracking data.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def report(events, output_path=None):
    """
    Generate a comprehensive report for all trials in an events file or DataFrame.
    The report includes trial statistics like duration, fixations, saccades, and saccade amplitudes.
    
    Parameters:
    -----------
    events (str or DataFrame): Path to events CSV file or pandas DataFrame with events data
    output_path (str, optional): Path to save the output report CSV file. If None and events is a path,
                                a path will be generated based on the input file.
    
    Returns:
    --------
    str or DataFrame: Path to the generated report file if output_path is provided or can be generated;
                     otherwise returns the DataFrame with the report
    """
    
    # Check if events is a file path or DataFrame
    if isinstance(events, pd.DataFrame):
        events_df = events
        print("Generating trial report from DataFrame")
        # If no output_path is provided, we'll return the DataFrame
        if output_path is None:
            return_df = True
        else:
            return_df = False
            output_path = Path(output_path)
    else:
        print(f"Generating trial report from: {events}")
        # Create output filename if not provided
        events_path = Path(events)
        if output_path is None:
            output_path = events_path.parent / f"{events_path.stem}_report.csv"
            return_df = False
        else:
            output_path = Path(output_path)
            return_df = False
        
        try:
            # Load events data
            events_df = pd.read_csv(events)
        except Exception as e:
            print(f"ERROR loading events file: {e}")
            return None
    
    try:
        # Check if required columns exist
        required_columns = ['trial', 'type', 'sttime', 'entime']
        for col in required_columns:
            if col not in events_df.columns:
                print(f"ERROR: Required column '{col}' not found in events file!")
                return None
        
        # Clean events data (remove NaN trials and empty columns)
        events_df = clean_dataframe(events_df)
            
        # Generate report
        report_df = create_report(events_df)
        
        # If output_path is provided or we're working with a file path, save to CSV
        if not return_df:
            report_df.to_csv(output_path, index=False)
            print(f"Report saved to: {output_path}")
            return str(output_path)
        else:
            # Return the DataFrame directly
            return report_df
            
    except Exception as e:
        print(f"ERROR generating report: {e}")
        return None


def clean_dataframe(df):
    """
    Clean a dataframe by removing rows with NaN trials and empty columns.
    
    Parameters:
    -----------
    df (DataFrame): Pandas DataFrame to clean
    
    Returns:
    --------
    DataFrame: Cleaned DataFrame
    """
    # Remove rows where 'trial' is NaN
    if 'trial' in df.columns:
        df = df.dropna(subset=['trial'])
    
    # Remove columns entirely NaN or zero
    cols_to_remove = []
    for col in df.columns:
        if df[col].isna().all():
            cols_to_remove.append(col)
        elif df[col].dtype in ['int64', 'float64']:
            if df[col].dropna().eq(0).all() and not df[col].dropna().empty:
                cols_to_remove.append(col)
    
    if cols_to_remove:
        df_cleaned = df.drop(columns=cols_to_remove)
        print(f"Removed {len(cols_to_remove)} empty or zero-filled columns")
    else:
        df_cleaned = df
        
    return df_cleaned


def create_report(events_df):
    """
    Create a comprehensive report for all trials.
    
    Parameters:
    -----------
    events_df (DataFrame): Cleaned events DataFrame
    
    Returns:
    --------
    DataFrame: Report DataFrame with trial statistics
    """
    report_data = []
    unique_trials = events_df['trial'].unique()
    
    print(f"Processing {len(unique_trials)} trials...")
    
    for trial in unique_trials:
        trial_data = events_df[events_df['trial'] == trial]
        
        # Recording duration
        trial_start = trial_data['sttime'].min()
        trial_end = trial_data['entime'].max()
        recording_duration = trial_end - trial_start
        
        # Total number of samples (count of all events in the trial)
        total_samples = trial_data.shape[0]
        
        # Number of fixations
        num_fixations = trial_data[trial_data['type'] == 'ENDFIX'].shape[0]
        
        # Number of saccades
        num_saccades = trial_data[trial_data['type'] == 'ENDSACC'].shape[0]
        
        # Number of blinks
        num_blinks = trial_data[trial_data['type'] == 'ENDBLINK'].shape[0] if 'ENDBLINK' in trial_data['type'].values else 0
        
        # Average fixation duration
        fixation_durations = (trial_data[trial_data['type'] == 'ENDFIX']['entime'] - 
                              trial_data[trial_data['type'] == 'ENDFIX']['sttime'])
        avg_fixation_duration = fixation_durations.mean() if not fixation_durations.empty else np.nan
        
        # Average saccade amplitude (in degrees)
        saccades = trial_data[trial_data['type'] == 'ENDSACC']
        if not saccades.empty:
            # Check if all required columns exist
            saccade_cols = ['genx', 'gstx', 'geny', 'gsty', 'supd_x', 'eupd_x', 'supd_y', 'eupd_y']
            if all(col in saccades.columns for col in saccade_cols):
                # Calculate pixel distances (Euclidean distance between start and end gaze positions)
                pixel_distances = np.sqrt((saccades['genx'] - saccades['gstx']) ** 2 +
                                          (saccades['geny'] - saccades['gsty']) ** 2)
                
                # Calculate average units-per-degree for each saccade
                avg_units_per_degree = (saccades['supd_x'] + saccades['eupd_x'] +
                                        saccades['supd_y'] + saccades['eupd_y']) / 4
                
                # Calculate saccade amplitude in degrees
                amplitudes_deg = pixel_distances / avg_units_per_degree
                avg_saccade_amplitude = amplitudes_deg.mean()
            else:
                avg_saccade_amplitude = np.nan
        else:
            avg_saccade_amplitude = np.nan
        
        # Add to report data
        report_data.append({
            'trial': trial,
            'recording_duration': recording_duration,
            'total_samples': total_samples,
            'num_fixations': num_fixations,
            'num_saccades': num_saccades,
            'num_blinks': num_blinks,
            'avg_fixation_duration': avg_fixation_duration,
            'avg_saccade_amplitude': avg_saccade_amplitude
        })
    
    # Create report DataFrame
    report_df = pd.DataFrame(report_data)
    return report_df
