import pyaudio       # Handles microphone input
import wave          # Allows saving audio in WAV format

def record_audio(filename="audio/recording.wav", duration=5): #Output and duration for our recording
    """
    Records audio from your microphone and saves it as a .wav file.

    Parameters:
    - filename: where the recorded audio should be saved
    - duration: how long (in seconds) to record
    """

    chunk = 1024               # Size of each audio buffer (1024 frames)
    format = pyaudio.paInt16   # Format: 16-bit PCM encoding (standard audio format)
    channels = 1               # 1 = mono input (1 microphone), 2 = stereo
    rate = 44100               # Sample rate (samples/second). 44100 = CD-quality audio

    p = pyaudio.PyAudio()      # Initialize the PyAudio engine
    #Turn on the microphone system (the control board)

    # Open a stream to capture audio from the microphone
    stream = p.open(                # 🎙️ Open a live mic wire (your channel to listen through)
        format=format,              # Audio format (16-bit)
        channels=channels,          # Mono or Stereo
        rate=rate,                  # How fast to collect samples
        input=True,                 # True = mic input
        frames_per_buffer=chunk     # How many frames per chunk
    )

    print("Recording started...")

    frames = []  # This list will collect each chunk of audio data

    # Loop for the duration: collect (rate / chunk) chunks per second
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)  # Read one chunk of audio from the mic
        frames.append(data)        # Store that chunk in the list

    print("Recording finished.")

    # Cleanup: stop the mic stream and close it
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data to a .wav file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)                            # Set to mono
        wf.setsampwidth(p.get_sample_size(format))           # Auto-detect size from format
        wf.setframerate(rate)                                # Set sample rate
        wf.writeframes(b''.join(frames))                     # Join all chunks and write to file


# Run directly for testing
if __name__ == "__main__":
    record_audio(duration=5)  # record 5 seconds of audio
