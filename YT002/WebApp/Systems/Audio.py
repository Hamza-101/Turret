# See if edge conditions okay
import pyaudio
import threading

# Audio parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 2  # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100  # Sample rate (samples per second)
CHUNK = 1024  # Size of each audio chunk

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Create a stream for output (playback)
stream_output = audio.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True)

# Create a stream for input (recording)
stream_input = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

# Flag to control the recording loop
recording = False

def record_and_playback():
    global recording
    while recording:
        # Read a chunk of data from the microphone
        data = stream_input.read(CHUNK)

        # Write the data to the output stream (playback)
        stream_output.write(data)

def start_recording():
    global recording
    recording = True
    threading.Thread(target=record_and_playback).start()

def stop_recording():
    global recording
    recording = False

# Example of controlling the recording with a button press
try:
    while True:
        user_input = input("Press 'r' to start/stop recording: ")
        if user_input.lower() == 'r':
            if not recording:
                print("Recording started...")
                start_recording()
            else:
                print("Recording stopped.")
                stop_recording()
except KeyboardInterrupt:
    pass

# Cleanup
stream_input.stop_stream()
stream_input.close()
stream_output.stop_stream()
stream_output.close()
audio.terminate()
