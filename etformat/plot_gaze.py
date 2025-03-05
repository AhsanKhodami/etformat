import matplotlib.pyplot as plt

def plot_gaze(samples, trial_number, screen_width=2560, screen_height=1440):
    """
    Plots gaze movement for a given trial using x and y positions from samples.

    Parameters:
    -----------
    samples : DataFrame
        The dataframe containing gaze sample data.
    trial_number : int
        The exact trial number to plot.
    screen_width : int, default=2560
        Width of the screen in pixels.
    screen_height : int, default=1440
        Height of the screen in pixels.
    """
    # Notify user about default screen size
    if screen_width == 2560 and screen_height == 1440:
        print("⚠️ Default screen size is 2560x1440. If incorrect, specify `screen_width` and `screen_height`.")

    # Fix missing trial numbers by forward-filling
    samples = samples.copy()
    samples["trial"] = samples["trial"].ffill()


    # Map actual trials without shifting them
    unique_trials = sorted(samples["trial"].dropna().unique())
    
    # Ensure the requested trial number exists
    if trial_number not in unique_trials:
        print(f"⚠️ Trial {trial_number} not found in data. Available trials: {unique_trials[:5]} ... {unique_trials[-5:]}")
        return

    # Determine recorded eye
    eye_recorded = "unknown"
    if "gxL" in samples.columns and "gxR" in samples.columns:
        eye_recorded = "both"
    elif "gxR" in samples.columns:
        eye_recorded = "right"
    elif "gxL" in samples.columns:
        eye_recorded = "left"

    if eye_recorded == "unknown":
        print("⚠️ No gaze position data found in samples!")
        return

    # Choose gaze position columns
    if eye_recorded == "both":
        x_col, y_col = ["gxR", "gyR"]  # Default to right eye
    elif eye_recorded == "right":
        x_col, y_col = ["gxR", "gyR"]
    else:
        x_col, y_col = ["gxL", "gyL"]

    # Extract correct trial data
    trial_data = samples[samples["trial"] == trial_number-1]
    #if trial_data becomes 0, trial_data  is 1
    

    if trial_data.empty:
        print(f"⚠️ No gaze data found for trial {trial_number}")
        return

    # Extract gaze positions
    gaze_x = trial_data[x_col]
    gaze_y = screen_height - trial_data[y_col]  # Flip Y-axis for screen coordinates

    gaze_count = len(trial_data)

    # Print trial info
    print(f"✅ Trial {trial_number} has {gaze_count} gaze points.")

    # Plot gaze path as a continuous line
    plt.figure(figsize=(10, 6))
    plt.plot(gaze_x, gaze_y, linestyle='-', color='blue', alpha=0.6)  # Line only
    plt.xlim(0, screen_width)
    plt.ylim(0, screen_height)
    plt.xlabel("X Position (pixels)")
    plt.ylabel("Y Position (pixels)")
    plt.title(f"Gaze Path in Trial {trial_number}")

    # Save and show plot
    # plt.savefig(f'gaze_plot_trial_{trial_number}.png', dpi=1200)
    plt.show()
