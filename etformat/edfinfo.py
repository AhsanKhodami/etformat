import os
import re
from .edffile import EDFFile

def edfinfo(edf_file_path):
    """
    Extracts and prints details about an EDF file in a readable format, 
    ensuring all values come directly from the file.

    Parameters:
    -----------
    edf_file_path : str
        Path to the EDF file.

    Returns:
    --------
    None (prints the formatted details)
    """
    try:
        # Ensure absolute path resolution
        edf_file_path = os.path.abspath(edf_file_path)

        # Check if the file exists
        if not os.path.isfile(edf_file_path):
            print(f"❌ Error: The file '{edf_file_path}' does not exist. Check the path and try again.")
            return

        # Load EDF file
        edf = EDFFile(edf_file_path, loadevents=True, loadsamples=True)

        if edf.recordings.empty:
            print("⚠️ No recording information found in the EDF file.")
            return

        # Extract first recording entry
        first_recording = edf.recordings.iloc[0]

        # Extract relevant details
        eye = first_recording.get('eye', "Unknown")
        sample_rate = first_recording.get('sample_rate', "Unknown")
        pupil_type = first_recording.get('pupil_type', "Unknown")
        recording_mode = first_recording.get('recording_mode', "Unknown")
        record_type = first_recording.get('record_type', "Unknown")
        calibration_type = "Unknown"

        # Extract EyeLink version (correctly parsed from preamble)
        preamble_lines = edf.preamble.split("\n") if edf.preamble else []
        recorded_by = "Unknown"
        record_date = "Unknown"
        screen_width, screen_height = "Unknown", "Unknown"
        serial_number = "Unknown"
        camera_version = "Unknown"
        eyelink_version = "Unknown"

        for line in preamble_lines:
            line = line.strip()

            # Extract "Recorded By"
            if line.startswith("** RECORDED BY"):
                recorded_by = line.replace("** RECORDED BY", "").strip()

            # Extract Recording Date (Fix Format)
            elif line.startswith("** DATE:"):
                record_date = line.replace("** DATE:", "").strip()

            # Extract EyeLink Version
            elif line.startswith("** VERSION:") or line.startswith("** SOURCE:"):
                eyelink_version = line.replace("** VERSION:", "").replace("** SOURCE:", "").strip()

            # Extract Serial Number
            elif line.startswith("** SERIAL NUMBER:"):
                serial_number = line.replace("** SERIAL NUMBER:", "").strip()

            # Extract Camera Version
            elif line.startswith("** CAMERA:"):
                camera_version = line.replace("** CAMERA:", "").strip()

        # Extract Screen Resolution from Event Messages (DISPLAY_COORDS)
        for _, row in edf.events.iterrows():
            if isinstance(row['message'], str):
                if "DISPLAY_COORDS" in row['message']:
                    match = re.search(r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", row['message'])
                    if match:
                        screen_width = int(match.group(3)) + 1
                        screen_height = int(match.group(4)) + 1
                elif "!CAL" in row['message'] and "CALIBRATION" in row['message']:
                    cal_match = re.search(r"CALIBRATION \(([^,]+)", row['message'])
                    if cal_match:
                        calibration_type = cal_match.group(1).strip()

        # Print the formatted information
        print("📄 **EDF File Information**")
        print("=" * 50)
        print(f"📌 Eye Recorded      : {eye}")
        print(f"📌 Sampling Rate     : {sample_rate} Hz")
        print(f"📌 Pupil Measurement : {pupil_type}")
        print(f"📌 Recording Mode    : {recording_mode}")
        print(f"📌 Data Type         : {record_type}")
        print(f"📌 Calibration Type  : {calibration_type}")
        print(f"📌 Screen Size       : {screen_width} x {screen_height} pixels")
        print(f"📌 EyeLink Version   : {eyelink_version}")
        print(f"📌 Camera Version    : {camera_version}")
        print(f"📌 Serial Number     : {serial_number}")
        print(f"📌 Recorded By       : {recorded_by}")
        print(f"📌 Recording Date    : {record_date}")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error reading EDF file: {str(e)}")
