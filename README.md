# PyShazam

PyShazam is a Python script that uses the Shazam API to capture audio from a microphone, identify the song being played, and display its album art cover. The script runs on Raspberry Pi or macOS devices.

## Requirements

- Python 3.7 or above
- `pyaudio` library for audio capturing
- `wave` library for working with WAV audio files
- `shazamio` library for interacting with the Shazam API
- `Pillow` library for displaying album art images
- `pydub` library for audio file handling
- `time` library for managing delays
- `urllib` library for opening URLs
- `os` library for file operations

## Installation

1. Install Python 3: Visit the official Python website (https://www.python.org) and follow the instructions to download and install Python 3 for your operating system.

2. Install the required libraries: Open a terminal or command prompt and run the following command to install the necessary libraries:
```
pip install pyaudio wave shazamio Pillow pydub
```

## Usage

1. Make sure you have a working microphone connected to your Raspberry Pi or macOS device.

2. Run the `pyshazam.py` script using Python:
```
python pyshazam.py
```


3. The script will start capturing audio from the microphone for 10 seconds at a time.

4. After each audio capture, the script will send the audio data to the Shazam API for song identification.

5. If a match is found, the script will display the album art cover of the identified song.

6. The script will wait for 10 seconds before capturing audio again.

7. To stop the script, press `Ctrl + C` in the terminal or command prompt.

## Customization

- You can adjust the duration of each audio capture by modifying the `capture_audio` function in the script.

- Additional customization options can be explored by referring to the documentation of the used libraries:
- `pyaudio`: https://people.csail.mit.edu/hubert/pyaudio/docs/
- `wave`: https://docs.python.org/3/library/wave.html
- `shazamio`: https://github.com/fr31/shazamio
- `Pillow`: https://pillow.readthedocs.io/en/stable/
- `pydub`: https://github.com/jiaaro/pydub

## License

This script is licensed under the [MIT License](https://opensource.org/licenses/MIT).

