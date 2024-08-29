from pathlib import Path

# Function to get the Downloads directory path
def get_download_dir():
    # Get the home directory of the current user
    home_dir = Path.home()
    # Construct the path to the Downloads folder
    download_dir = home_dir / "Downloads" / "YouTubeDownloader"
    return download_dir

# Directory for downloads
DOWNLOAD_DIR = str(get_download_dir())  # Set the directory where the videos will be saved

# System configuration settings
def configure_system():
    from pydub import AudioSegment  # Import AudioSegment for audio conversion

