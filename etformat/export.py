import os
import pandas as pd
from .edffile import EDFFile

def convert_edf_to_csv(
    edf_filepath,
    consistency=2,
    loadevents=True,
    loadsamples=True,
    sample_fields=None,
    parse_events="all",
    wide_variables=True,
    trigger_marker="TRIGGER",
    libpath=None
):
    """
    Converts an EDF file into separate CSV files for events and samples.
    Output files are saved in the same directory as the EDF file.

    Parameters
    ----------
    edf_filepath : str
        Path to the EDF file.
    consistency : int, default=2
        Consistency check control.
    loadevents : bool, default=True
        Whether to load events from the EDF file.
    loadsamples : bool, default=True
        Whether to load samples from the EDF file.
    sample_fields : list or None
        Fields to include in the samples DataFrame.
    parse_events : str or list, default="all"
        Specifies which events to parse.
    wide_variables : bool, default=True
        Whether to pivot variables to wide format.
    trigger_marker : str, default="TRIGGER"
        Marker string for triggers.
    libpath : str, default=None
        Path to the EDF API library.

    Returns
    -------
    None
    """
    # Ensure absolute path resolution
    edf_filepath = os.path.abspath(edf_filepath)

    if not os.path.isfile(edf_filepath):
        raise FileNotFoundError(f"Error: The file '{edf_filepath}' does not exist. Check the path and try again.")

    # Determine output directory as the same location as the EDF file
    output_dir = os.path.dirname(edf_filepath)
    edf_basename = os.path.splitext(os.path.basename(edf_filepath))[0]

    # Load the EDF file
    edf_file = EDFFile(
        filename=edf_filepath,
        consistency=consistency,
        loadevents=loadevents,
        loadsamples=loadsamples,
        sample_fields=sample_fields,
        parse_events=parse_events,
        wide_variables=wide_variables,
        trigger_marker=trigger_marker,
        verbose=True,  # Automatically set verbose to True
        libpath=libpath,
    )

    # Save events to CSV if available
    if loadevents and hasattr(edf_file, "events"):
        events_csv_path = os.path.join(output_dir, f"{edf_basename}_events.csv")
        edf_file.events.to_csv(events_csv_path, index=False)
        print(f"Events saved to: {events_csv_path}")

    # Save samples to CSV if available
    if loadsamples and hasattr(edf_file, "samples"):
        edf_file.samples["trial"] = edf_file.samples["trial"].ffill()
        if edf_file.samples["trial"].min() == 0:  
            edf_file.samples["trial"] += 1  # Shift trials forward if needed

        samples_csv_path = os.path.join(output_dir, f"{edf_basename}_samples.csv")
        edf_file.samples.to_csv(samples_csv_path, index=False)
        print(f"Samples saved to: {samples_csv_path}")

def export(edf_filepath):
    """
    Exports an EDF file to CSV format.
    The output files are saved in the same directory as the EDF file.

    Parameters:
    -----------
    edf_filepath : str
        Path to the EDF file to be converted.
    """
    # Resolve the absolute path if the user provides a relative path
    edf_filepath = os.path.abspath(edf_filepath)
    
    # Ensure the file exists
    if not os.path.isfile(edf_filepath):
        raise FileNotFoundError(f"Error: The file '{edf_filepath}' does not exist. Check the path and try again.")

    # Convert EDF to CSV
    convert_edf_to_csv(edf_filepath)
