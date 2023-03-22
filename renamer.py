import os
import sys
import re

__version__ = "0.1.0"

# Check if the script is running as a standalone executable
if getattr(sys, 'frozen', False):
    # Change the current working directory to the directory of the executable
    os.chdir(os.path.dirname(sys.executable))

# Function to extract the episode number from a given filename
def extract_episode_number(filename):
    # Try to find the episode number using the first regex pattern (e.g. S01E01 or E01)
    match = re.search(r'(?:S\d{1,2}E|E)(\d{1,2})', filename, re.IGNORECASE)
    if match:
        # If a match is found, return the episode number as an integer
        return int(match.group(1))
    else:
        # If no match is found, try the second regex pattern (e.g. 01.)
        match = re.search(r'^(\d{1,2})\.', filename, re.IGNORECASE)
        # If a match is found, return the episode number as an integer, otherwise return None
        return int(match.group(1)) if match else None

# Lists of video and subtitle file extensions
video_extensions = ['.mkv', '.mp4', '.MKV', '.MP4']
subtitle_extensions = ['.ass', '.ssa', '.srt', '.ASS', '.SRT', '.SSA', '.sub', '.SUB']

# Get a list of video files in the current directory that match the specified extensions and are larger than 200MB
video_files = [f for f in os.listdir() if any(f.endswith(ext) for ext in video_extensions) and os.path.getsize(f) > 200 * 1024 * 1024]
# Get a list of subtitle files in the current directory that match the specified extensions
subtitle_files = [f for f in os.listdir() if any(f.endswith(ext) for ext in subtitle_extensions)]

# Check if the number of video files matches the number of subtitle files
if len(video_files) == len(subtitle_files):
    # Initialize an empty list to store rename operations
    rename_operations = []

    # Create a dictionary with episode numbers as keys and video filenames as values
    video_files_dict = {extract_episode_number(f): f for f in video_files}

    # Loop through each subtitle file
    for subtitle_file in subtitle_files:
        # Extract the episode number from the subtitle file
        episode_number = extract_episode_number(subtitle_file)
        # Check if the episode number exists in the video_files_dict
        if episode_number in video_files_dict:
            # Get the corresponding video file
            video_file = video_files_dict[episode_number]
            # Split the video file name into name and extension
            video_name, video_ext = os.path.splitext(video_file)
            # Split the subtitle file name into name and extension
            subtitle_name, subtitle_ext = os.path.splitext(subtitle_file)
            # Create a new subtitle name by combining the video name and subtitle extension
            new_subtitle_name = video_name + subtitle_ext
            # Add the rename operation (old name, new name) to the rename_operations list
            rename_operations.append((subtitle_file, new_subtitle_name))

    # Sort the rename_operations list by episode number
    rename_operations.sort(key=lambda x: extract_episode_number(x[0]))

    # Check if there are any rename operations
    if not rename_operations:
        # If not, print a message and exit the program
        print("No matching video and subtitle files found. Exiting.")
        exit()

    # Perform the rename operations and print the results
    for old_name, new_name in rename_operations:
        # Rename the subtitle file
        os.rename(old_name, new_name)
        # Print the old and new names of the renamed subtitle file
        print(f"Renamed: {old_name} -> {new_name}")
else:
    # If the number of video files and subtitle files do not match, print a message with the counts
    print(f"Numbers of video files and subtitle files do not match. Video files found: {len(video_files)}, subtitle files found: {len(subtitle_files)}")
