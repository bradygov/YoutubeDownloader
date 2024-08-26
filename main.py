import tkinter
import customtkinter
from downloader import startDownload  # Import the function responsible for downloading videos
from settings import DOWNLOAD_DIR, configure_system  # Import settings and configuration function

# Configure system settings such as ffmpeg path
configure_system()

# Create the main application window
app = customtkinter.CTk()
app.geometry('720x480')  # Set the window size
app.title('YouTube Downloader')  # Set the window title

# Add a label to the window for instructions
title = customtkinter.CTkLabel(app, text='Insert a YouTube link')
title.pack(padx=10, pady=10)  # Add padding around the label

# Add an entry widget where the user can input the YouTube URL
url_var = tkinter.StringVar()  # Create a Tkinter string variable to hold the URL
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)  # Entry widget for the URL
link.pack()  # Place the entry widget in the window

# Add a label that will display the status of the download (e.g., "Download Complete" or "Download Error")
finshLabel = customtkinter.CTkLabel(app, text='')
finshLabel.pack()  # Place the status label in the window

# Add a label that will display the percentage of the download progress
pPercentage = customtkinter.CTkLabel(app, text='0%')
pPercentage.pack()  # Place the progress percentage label in the window

# Add a progress bar that will visually show the download progress
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)  # Initialize the progress bar to 0%
progressBar.pack(padx=10, pady=10)  # Add padding around the progress bar

# Add radio buttons for format selection (MP4 or MP3)
format_var = tkinter.StringVar(value='MP4')  # Create a Tkinter string variable with default value 'MP4'
mp4_radio = customtkinter.CTkRadioButton(app, text='MP4', variable=format_var, value='MP4')  # MP4 option
mp4_radio.pack(padx=10, pady=5)
mp3_radio = customtkinter.CTkRadioButton(app, text='MP3', variable=format_var, value='MP3')  # MP3 option
mp3_radio.pack(padx=10, pady=5)

# Add a download button that triggers the download process when clicked
download = customtkinter.CTkButton(app, text='Download', command=lambda: startDownload(link.get(), format_var.get(), title, finshLabel, pPercentage, progressBar))
download.pack(padx=10, pady=10)

# Start the application's main loop, waiting for user interaction
app.mainloop()
