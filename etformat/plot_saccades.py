import matplotlib.pyplot as plt

def plot_saccades(events, trial_number=0, screen_width=2560, screen_height=1440):
    """
    Plots saccades for a given trial on a user-defined screen with numbered points and directional arrows.
    If the user does not specify screen size, it defaults to 2560x1440 and informs the user.

    Parameters:
    -----------
    events : DataFrame
        The dataframe containing event data.
    trial_number : int, default=0
        The trial number to filter and plot (automatically adjusted if necessary).
    screen_width : int, default=2560
        Width of the screen in pixels. Defaults to 2560.
    screen_height : int, default=1440
        Height of the screen in pixels. Defaults to 1440.
    """
    # Notify the user if the default screen size is being used
    if screen_width == 2560 and screen_height == 1440:
        print("⚠️ Default screen size is 2560x1440. If incorrect, specify `screen_width` and `screen_height` in the function call.")

    # Adjust trial number indexing if needed
    if events["trial"].min() == 0:
        trial_number -= 1  # Adjust indexing if trial numbering starts from 0

    # Filter for ENDSACC events in the specified trial
    saccades = events[(events['type'] == 'ENDSACC') & (events['trial'] == trial_number-1)]

    if saccades.empty:
        print(f"No saccades found for trial {trial_number}")
        return

    # Extract gaze start and end positions
    start_x = saccades['gstx']
    start_y = screen_height - saccades['gsty']  # Flip Y-axis for screen coordinates
    end_x = saccades['genx']
    end_y = screen_height - saccades['geny']  # Flip Y-axis for screen coordinates

    gaze_count = len(saccades)  # Count number of gaze movements

    # Print the gaze count as normal text
    print(f"Trial {trial_number} has {gaze_count} gaze movements.")

    # Plot saccades
    plt.figure(figsize=(10, 6))
    plt.xlim(0, screen_width)
    plt.ylim(0, screen_height)
    plt.xlabel("X Position (pixels)")
    plt.ylabel("Y Position (pixels)")
    plt.title(f"Saccades in Trial {trial_number}")

    # Draw saccade lines with arrows and numbering
    for i, (sx, sy, ex, ey) in enumerate(zip(start_x, start_y, end_x, end_y), start=1):
        plt.text(sx, sy, str(i), fontsize=10, color='blue', alpha=0.45, ha='center', va='center')
        plt.arrow(sx, sy, ex - sx, ey - sy, head_width=20, head_length=20, fc='red', ec='red')

    # plt.savefig('saccades.png', dpi=1200)
    plt.show()
