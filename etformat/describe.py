import os
import pandas as pd
from .edffile import EDFFile

def describe(data_source, trial_number=None):
    """
    Computes statistics for a given trial or all trials.
    Supports both direct EDF file input or preloaded event & sample DataFrames.

    Parameters:
    -----------
    data_source : str or tuple of (events, samples)
        - If str: Path to the EDF file (absolute or relative).
        - If tuple: A tuple containing (events DataFrame, samples DataFrame).
    trial_number : int or None, default=None
        If specified, provides statistics for only the given trial.
        If None, provides statistics for all trials.

    Returns:
    --------
    - If a single trial is requested, returns a dictionary of computed statistics.
    - If all trials are requested, returns a DataFrame with statistics for each trial.
    """
    try:
        # Case 1: User provides an EDF file path
        if isinstance(data_source, str):
            edf_file_path = os.path.abspath(data_source)

            if not os.path.isfile(edf_file_path):
                print(f"❌ Error: The file '{edf_file_path}' does not exist. Check the path and try again.")
                return None

            # Load EDF file
            edf = EDFFile(edf_file_path, loadevents=True, loadsamples=True)

            if edf.samples is None or edf.events is None:
                print("⚠️ No valid sample or event data found in the EDF file.")
                return None

            samples = edf.samples.copy()
            events = edf.events.copy()

        # Case 2: User provides DataFrame inputs (events, samples)
        elif isinstance(data_source, tuple) and len(data_source) == 2:
            events, samples = data_source
            if not isinstance(events, pd.DataFrame) or not isinstance(samples, pd.DataFrame):
                print("❌ Error: Expected (events DataFrame, samples DataFrame) as input.")
                return None
        else:
            print("❌ Error: Invalid input. Provide either an EDF file path or (events, samples) DataFrames.")
            return None

        # Ensure 'trial' column exists
        if "trial" not in samples.columns or "trial" not in events.columns:
            print("❌ Error: Missing 'trial' column in one of the input DataFrames.")
            return None

        # Ensure 'type' column exists in events before processing
        if "type" not in events.columns:
            print("❌ Error: Missing 'type' column in events DataFrame. Check CSV file.")
            return None

        # Ensure trials are filled properly
        samples["trial"] = samples["trial"].ffill()  # Fix for FutureWarning

        unique_trials = sorted(events["trial"].dropna().unique())

        if trial_number is None:
            trials_to_analyze = unique_trials
        else:
            if trial_number not in unique_trials:
                print(f"⚠️ Warning: Trial {trial_number} not found in the data.")
                return None
            trials_to_analyze = [trial_number]

        trial_data = []

        for trial in trials_to_analyze:
            trial_samples = samples[samples["trial"] == trial - 1]
            trial_events = events[events["trial"] == trial - 1]

            trial_duration = trial_samples["time"].max() - trial_samples["time"].min() if not trial_samples.empty else None

            num_fixations = len(trial_events[trial_events["type"] == "ENDFIX"])
            num_saccades = len(trial_events[trial_events["type"] == "ENDSACC"])
            num_blinks = len(trial_events[trial_events["type"] == "ENDBLINK"])

            avg_fixation_duration = (trial_duration / num_fixations) if num_fixations > 0 else None

            if num_saccades > 0:
                saccade_amplitudes = ((trial_events[trial_events["type"] == "ENDSACC"]["genx"] - 
                                       trial_events[trial_events["type"] == "ENDSACC"]["gstx"]) ** 2 +
                                      (trial_events[trial_events["type"] == "ENDSACC"]["geny"] - 
                                       trial_events[trial_events["type"] == "ENDSACC"]["gsty"]) ** 2) ** 0.5
                avg_saccade_amplitude = saccade_amplitudes.mean() * 10e-3
            else:
                avg_saccade_amplitude = None

            trial_data.append({
                "Trial": trial,
                "Total Duration (ms)": trial_duration,
                "Total Samples": len(trial_samples),
                "Number of Fixations": num_fixations,
                "Number of Saccades": num_saccades,
                "Number of Blinks": num_blinks,
                "Avg Fixation Duration (ms)": avg_fixation_duration,
                "Avg Saccade Amplitude": avg_saccade_amplitude
            })

        results_df = pd.DataFrame(trial_data)

        if trial_number is not None:
            return results_df.iloc[0].to_dict()
        else:
            return results_df

    except Exception as e:
        print(f"❌ Error processing data: {str(e)}")
        return None
