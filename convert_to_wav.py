from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")
    print(f"Converted {mp3_path} → {wav_path}")

# Test run (only runs if called directly)
if __name__ == "__main__":
    convert_mp3_to_wav("output/tts_output.mp3", "output/tts_output.wav")
