from recorder import record_audio
from transcriber import transcribe_audio
from tts import synthesize_speech
from convert_to_wav import convert_mp3_to_wav


def main():
    print("Starting recording...")

    # Step 1: Record audio (5 seconds, default location)
    record_audio()  # saves to audio/recording.wav

    print("Transcribing recorded audio...")

    # Step 2: Transcribe the recorded audio
    transcript = transcribe_audio("audio/recording.wav")
    print("Transcription complete.")
    print("Transcript:", transcript)

    print("Generating speech from transcript...")

    # Step 3: Synthesize voice from transcript
    synthesize_speech(transcript)

    print("Done! Audio and transcript saved in /output under specified file")

    convert_mp3_to_wav("output/tts_output.mp3", "output/tts_output.wav")

    print("Done! mp3 file converted alternatively to wav!")


if __name__ == "__main__":
    main()
