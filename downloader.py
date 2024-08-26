import os
import threading
from pytubefix import YouTube, Playlist  # Import YouTube and Playlist classes from pytubefix
from pydub import AudioSegment  # Import AudioSegment for audio conversion
from pydub.exceptions import CouldntDecodeError  # Import exception for handling decode errors
from settings import DOWNLOAD_DIR  # Import the directory where downloads will be saved

# Function to start the download process
def startDownload(url, format_choice, title, finshLabel, pPercentage, progressBar):
    """
    Starts the download process for a single video or a playlist.
    """
    try:
        if 'playlist' in url:  # Check if the URL is a playlist
            playlist = Playlist(url)  # Create a Playlist object
            total_videos = len(playlist.videos)  # Get the total number of videos in the playlist
            completed_videos = 0  # Initialize the number of completed downloads
            progressBar.set(0)  # Reset the progress bar
            # Start downloading the playlist videos in a separate thread
            threading.Thread(target=download_video, args=(playlist.videos, format_choice, title, finshLabel, pPercentage, progressBar, total_videos)).start()
        else:  # If the URL is for a single video
            ytObject = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, pPercentage, progressBar))
            total_videos = 1  # Set the total number of videos to 1
            completed_videos = 0  # Initialize the number of completed downloads
            progressBar.set(0)  # Reset the progress bar
            # Start downloading the video in a separate thread
            threading.Thread(target=download_video, args=([ytObject], format_choice, title, finshLabel, pPercentage, progressBar, total_videos)).start()
    except Exception as e:
        print(f"Error in startDownload: {e}")  # Print the error for debugging
        finshLabel.configure(text='Download Error!', text_color='red')  # Update the UI with an error message

# Function to handle the download and conversion process for each video
def download_video(videos, format_choice, title, finshLabel, pPercentage, progressBar, total_videos):
    """
    Downloads and converts each video in the list of videos.
    """
    completed_videos = 0  # Initialize the number of completed downloads
    for video in videos:  # Iterate over each video in the list
        try:
            ytObject = video if isinstance(video, YouTube) else YouTube(video)  # Create a YouTube object if needed
            file_extension = 'mp4' if format_choice == 'MP4' else 'mp4'  # Set the file extension
            title.configure(text=f'Downloading: {ytObject.title}', text_color='white')  # Update the UI with the current video title
            finshLabel.configure(text='')  # Clear any previous messages
            if not os.path.exists(DOWNLOAD_DIR):  # Create the download directory if it doesn't exist
                os.makedirs(DOWNLOAD_DIR)
            filename = f"{ytObject.title}.{file_extension}"  # Create the filename
            file_path = os.path.join(DOWNLOAD_DIR, filename)  # Create the full file path
            ytObject.streams.get_highest_resolution().download(output_path=DOWNLOAD_DIR, filename=filename)  # Download the video

            if format_choice == 'MP3':  # If the user selected MP3 format
                mp3_file_path = file_path.replace('.mp4', '.mp3')  # Create the MP3 file path
                try:
                    audio = AudioSegment.from_file(file_path, format='mp4')  # Load the downloaded mp4 file
                    audio.export(mp3_file_path, format='mp3')  # Convert and save as MP3
                    os.remove(file_path)  # Remove the original mp4 file after successful conversion
                except CouldntDecodeError as e:
                    print(f"Error converting to MP3: {e}")  # Print the error for debugging
                    finshLabel.configure(text='Conversion Error!', text_color='red')  # Update the UI with an error message
                    continue  # Skip to the next video

            completed_videos += 1  # Increment the count of completed downloads
            percentage = (completed_videos / total_videos) * 100  # Calculate the completion percentage
            progressBar.set(completed_videos / total_videos)  # Update the progress bar
            pPercentage.configure(text=f'{int(percentage)}%')  # Update the percentage label
            if completed_videos == total_videos:  # If all videos are downloaded
                finshLabel.configure(text='All Downloads Complete!')  # Update the UI with a success message
            else:
                finshLabel.configure(text=f'Downloaded {completed_videos}/{total_videos}')  # Update the UI with progress
        except Exception as e:
            print(f"Error in download_single_video: {e}")  # Print the error for debugging
            finshLabel.configure(text='Download Error!', text_color='red')  # Update the UI with an error message

# Function to update the UI during the download process
def on_progress(stream, chunk, bytes_remaining, pPercentage, progressBar):
    """
    Updates the progress bar and percentage label during the download.
    """
    total_size = stream.filesize  # Get the total file size
    bytes_downloaded = total_size - bytes_remaining  # Calculate the number of bytes downloaded
    percentage_of_completion = bytes_downloaded / total_size * 100  # Calculate the completion percentage
    pPercentage.configure(text=f'{int(percentage_of_completion)}%')  # Update the percentage label
    pPercentage.update()  # Refresh the UI
    progressBar.set(float(percentage_of_completion) / 100)  # Update the progress bar
