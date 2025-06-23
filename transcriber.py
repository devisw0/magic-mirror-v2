from faster_whisper import WhisperModel

def transcribe_audio(transcribe_file: str) -> str:
    """
    Transcribes audio using the faster-whisper 'large-v2' model with GPU support.

    Parameters:
    - transcribe_file: path to the audio file

    Returns:
    - segment_text: full transcription result
    """

    print("Loading large-v2 model on GPU with float16...")

    # Load large-v2 model, cuda for GPU
    model = WhisperModel("medium", device="cuda", compute_type="int8_float16")   
    #use this once downloaded nvidia stuff
    #model = WhisperModel("large-v2", device="cpu", compute_type="int8")
    #More accurate but much more slower

    # Transcribing, beam search looks at 5 possible outputs
    segments, info = model.transcribe(transcribe_file, beam_size=1)
    # segments = generator (start, end, text), info = tuple (language, language_probability)

    # def generate_segments(audio_path):
    # waveform = load_audio(audio_path)
    # audio_chunks = split_waveform(waveform)

    # for chunk in audio_chunks:
    #     text = transcribe(chunk)
    #     yield Segment(start=..., end=..., text=text)

    print(f"Detected language: {info.language} ({info.language_probability * 100:.2f}% confidence from our model)")

    # Piecing together the text transcript
    segment_text = ""
    for segment in segments:
        segment_text += " " + segment.text

    # Save transcription to file
    with open("output/transcript.txt", "w", encoding="utf-8") as f:
        f.write(segment_text.strip())

    return segment_text


# ✅ Test mode: only runs when we run this file directly
if __name__ == "__main__":
    test_file = "output/tts_output.mp3"  # 👈 change if testing other files
    print("Transcribing:", test_file)
    result = transcribe_audio(test_file)
    print("\n Final Transcription:\n" + result)
