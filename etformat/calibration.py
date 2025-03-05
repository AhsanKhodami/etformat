import re
import numpy as np
import matplotlib.pyplot as plt
from .edffile import EDFFile

def calibration(edf_file_path):
    """
    Extracts calibration information from an EDF file.

    Parameters:
    -----------
    edf_file_path : str
        Path to the EDF file.

    Returns:
    --------
    None (prints calibration details and shows a plot)
    """
    try:
        # Load EDF file
        edf = EDFFile(edf_file_path, loadevents=True, loadsamples=False)

        if edf.events.empty:
            print("⚠️ No calibration data found in the EDF file.")
            return

        # Initialize storage variables
        calibrations = {}
        
        # Extract calibration data
        for _, row in edf.events.iterrows():
            if isinstance(row["message"], str):
                msg = row["message"]

                # Detect calibration event
                if "!CAL" in msg and "CALIBRATION" in msg:
                    model_match = re.search(r"CALIBRATION \(([^,]+),", msg)
                    eye_match = re.search(r"FOR (LEFT|RIGHT)", msg)

                    if model_match and eye_match:
                        eye = eye_match.group(1).strip()
                        model = model_match.group(1).strip()
                        calibrations[eye] = {
                            "model": model,
                            "errors": [],
                            "points": []
                        }

                # Detect calibration validation error
                elif "VALIDATION" in msg and "ERROR" in msg:
                    error_match = re.search(r"ERROR ([\d.]+) avg. ([\d.]+) max", msg)
                    eye_match = re.search(r"VALIDATION .*? (LEFT|RIGHT)", msg)
                    
                    if error_match and eye_match:
                        avg_error = float(error_match.group(1))
                        max_error = float(error_match.group(2))
                        eye = eye_match.group(1).strip()
                        if eye in calibrations:
                            calibrations[eye]["errors"].append((avg_error, max_error))

                # Detect calibration point offsets
                elif "VALIDATE" in msg and "OFFSET" in msg:
                    pos_match = re.search(r"at (\d+),(\d+)", msg)
                    offset_match = re.search(r"OFFSET ([\d.]+) deg.", msg)
                    eye_match = re.search(r"VALIDATE .*? (LEFT|RIGHT)", msg)

                    if pos_match and offset_match and eye_match:
                        x, y = float(pos_match.group(1)), float(pos_match.group(2))
                        offset = float(offset_match.group(1))
                        eye = eye_match.group(1).strip()
                        if eye in calibrations:
                            calibrations[eye]["points"].append((x, y, offset))

        # Process results for each eye separately
        for eye, data in calibrations.items():
            num_calibrations = len(data["errors"])
            avg_errors = [err[0] for err in data["errors"]]
            max_errors = [err[1] for err in data["errors"]]

            avg_error = np.mean(avg_errors) if avg_errors else "Unknown"
            max_error = np.max(max_errors) if max_errors else "Unknown"

            print(f"📌 Eye: {eye}")
            print(f"📌 Number of calibrations: {num_calibrations}")
            print(f"📌 Calibration Model: {data['model']}")
            print(f"📌 Average Error: {avg_error} degrees")
            print(f"📌 Max Error: {max_error} degrees")

            # Plot calibration points
            if data["points"]:
                x_positions = [p[0] for p in data["points"]]
                y_positions = [p[1] for p in data["points"]]
                offsets = [p[2] for p in data["points"]]

                # Fixing top-bottom inversion issue
                y_positions = [max(y_positions) - (y - min(y_positions)) for y in y_positions]

                plt.figure(figsize=(6, 4))
                plt.scatter(x_positions, y_positions, color="black", label="Target")
                plt.scatter(x_positions, y_positions, color="red", alpha=0.7, label="Measured")

                # Annotate errors
                for i, (x, y, offset) in enumerate(zip(x_positions, y_positions, offsets)):
                    plt.text(x, y, f"{offset:.2f}", fontsize=10, color="red")

                plt.xlabel("x (pixels)")
                plt.ylabel("y (pixels)")
                plt.title(f"Calibration ({eye.lower()} eye)")
                plt.legend()
                plt.show()

    except Exception as e:
        print(f"❌ Error extracting calibration data: {str(e)}")
