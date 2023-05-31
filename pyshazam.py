import pyaudio
import wave
from shazamio import Shazam
from PIL import Image
from pydub import AudioSegment
import time
from urllib.request import urlopen
import os

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

    # Save audio as a WAV file with timestamp in the file name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"audio.wav"

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename


# Function to identify the song using Shazam
async def identify_song(audio_file):
    shazam = Shazam()
    recognize_result = await shazam.recognize_song(audio_file)

    if recognize_result.get('matches'):
#    if 'matches' in recognize_result and len(recognize_result['matches']) > 0:    
#    if 'track' in recognize_result:
        song_info = recognize_result['track']
        album_art_url = song_info['images']['coverarthq']
        album_art = Image.open(urlopen(album_art_url))
        album_art.show()
    else:
        # Clear the previous album art
    #    album_art_label.configure(image="")
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
        print("No match found.")

    print("----- Matching Debug Information -----")
    print(f"Audio file: {audio_file}")
    print("Matching results:")
    print(recognize_result)
    print("--------------------------------------")


# Main function
def main():
    audio_file = "audio.wav"  # Initialize with a default audio file name
    while True:
        audio_file = capture_audio(10)  # Capture audio for 10 seconds and get the file name
        audio_data = AudioSegment.from_file(audio_file, format="wav")
        asyncio.run(identify_song(audio_data))
        os.remove(audio_file)  # Remove the previous audio file
        time.sleep(10)  # Wait for 10 seconds before capturing audio again


if __name__ == '__main__':
    import asyncio
    main()

