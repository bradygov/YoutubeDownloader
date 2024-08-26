# Directory for downloads
DOWNLOAD_DIR = 'D:\\python mp3'  # Set the directory where the videos will be saved

# System configuration settings
def configure_system():
    from pydub import AudioSegment  # Import AudioSegment for audio conversion
    # Set the path to ffmpeg if it's not in the system PATH
    AudioSegment.ffmpeg = "path_to_your_ffmpeg_executable"  # Update this to the correct path on your system
