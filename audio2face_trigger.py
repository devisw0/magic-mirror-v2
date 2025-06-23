from omni.kit.commands import execute

# Replace with actual audio path!
audio_path = "/absolute/path/to/your/output/tts_output.wav"

# Load and play audio
execute("SetAudioFile", file_path=audio_path)
execute("Play")
