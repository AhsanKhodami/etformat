from .edffile import EDFFile

def extract_channels(edf_file_path):
    """
    Extracts available channel names from an EDF file, filtering based on the recorded eye.

    Parameters:
    -----------
    edf_file_path : str
        Path to the EDF file.

    Returns:
    --------
    None (Prints the detected channels)
    """
    try:
        # Load EDF file
        edf = EDFFile(edf_file_path, loadevents=False, loadsamples=True)

        if edf.samples.empty:
            print("⚠️ No sample data found in the EDF file.")
            return
        
        # Determine the recorded eye from EDF metadata
        recorded_eye = "Unknown"
        if not edf.recordings.empty:
            recorded_eye = edf.recordings.iloc[0].get("eye", "Unknown")

        # Extract all available channels
        detected_channels = list(edf.samples.columns)

        # Separate general channels and eye-specific channels
        general_channels = [ch for ch in detected_channels if not ch.endswith(("L", "R"))]
        left_channels = [ch for ch in detected_channels if ch.endswith("L")]
        right_channels = [ch for ch in detected_channels if ch.endswith("R")]

        # Filter channels based on the recorded eye
        if recorded_eye == "LEFT":
            selected_channels = general_channels + left_channels
        elif recorded_eye == "RIGHT":
            selected_channels = general_channels + right_channels
        else:  # BOTH eyes
            selected_channels = detected_channels

        # Print the detected channels
        print("📌 **Detected Channels in EDF File**")
        print("=" * 50)
        print(f"📌 Recorded Eye: {recorded_eye}")
        print("=" * 50)
        for channel in selected_channels:
            print(f"  - {channel}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error extracting channels: {str(e)}")
