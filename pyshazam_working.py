import pyaudio
import wave
from shazamio import Shazam
from PIL import Image, ImageTk
from io import BytesIO
from pydub import AudioSegment
import time
from urllib.request import urlopen
import webbrowser
import os
import sys
os.environ["DISPLAY"] = ":0"
import tkinter as tk

# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# Change the working directory to the script's directory
os.chdir(script_dir)

# Function to capture audio from the microphone
def capture_audio(duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording audio...")
    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save audio as a WAV file
    filename = f"audio.wav"

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

# Function to identify the song using Shazam
async def identify_song(audio_file, window):
    global album_art_label  # Access the global variable
    global song_name_label

    shazam = Shazam()
    recognize_result = await shazam.recognize_song(audio_file)

    if 'track' in recognize_result:
        song_info = recognize_result['track']
        album_art_url = song_info['images']['coverarthq']
        album_art_data = urlopen(album_art_url).read()
        album_art_image = Image.open(BytesIO(album_art_data))
        album_art_image = album_art_image.resize((720, 720), Image.ANTIALIAS)
        album_art_photo = ImageTk.PhotoImage(album_art_image)

        # Update the label widget with the new image
        album_art_label.configure(image=album_art_photo)
        album_art_label.image = album_art_photo

        # Update the display
        window.update()

        # Update the song name label
        song_name = song_info['title']
        song_name_label.configure(text=song_name)
        song_name_label.update()  # Update the label to show the new text

    else:
        # Display fallback image when no match is found
        fallback_image = Image.open("no_match.png")
        fallback_photo = ImageTk.PhotoImage(fallback_image)

        # Update the label widget with the fallback image
        album_art_label.configure(image=fallback_photo)
        album_art_label.image = fallback_photo

        # Update the display
        window.update()

        # Clear the song name label
        song_name_label.configure(text="No match found")
        song_name_label.update() # Update the lable to show the new text

    print("----- Matching Debug Information -----")
    print(f"Audio file: {audio_file}")
    print("Matching results:")
    print(recognize_result)
#    print("***** SONG NAME ******")
#    print(song_name)
#    print("--------------------------------------")

# Main function
def main():
    # Create a tkinter window
    window = tk.Tk()
    window.title("Album Art Display")

    # Make the window full screen
    window.attributes('-fullscreen', True)

    # Set the screen width and height to 720
    screen_width = 720
    screen_height = 720
    window.geometry(f"{screen_width}x{screen_height}")

    # Create a label widget for the album art
    global album_art_label  # Declare it as a global variable
    global song_name_label 

    album_art_label = tk.Label(window)
    #album_art_label.pack()
    album_art_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    #album_art_label.pack(fill=tk.BOTH, expand=True)
    
    # Create a label widget for the song name
    #song_name_label = tk.Label(window, text="", font=("Arial", 20))
    #song_name_label.pack()

    song_name_label = tk.Label(window, text="", font=("Arial", 30), bg='white', fg='black')
    song_name_label.place(relx=0.05, rely=0.92, relwidth=0.9, relheight=0.07)

    while True:
        audio_file = capture_audio(8)  # Capture audio for 8 seconds and get the file name
        audio_data = AudioSegment.from_file(audio_file, format="wav")
        asyncio.run(identify_song(audio_file, window))
        os.remove(audio_file)  # Remove the previous audio file
        time.sleep(1)  # Wait for 1 seconds before capturing audio again

    # Destroy the tkinter window
    window.destroy()


if __name__ == '__main__':
    import asyncio
    main()

