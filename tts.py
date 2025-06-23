import requests
import os
from dotenv import load_dotenv
from pydub import AudioSegment


# 🟡 Load variables from the .env file
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

def synthesize_speech(text: str, output_path: str = "output/tts_output.mp3") -> None:
    """
    Converts text into speech using ElevenLabs Turbo v2.5 API and saves it.

    Parameters:
    - text: The text to convert to speech.
    - output_path: File path to save the MP3 audio output.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not API_KEY or not VOICE_ID:
        print("Missing API key or Voice ID. Check your .env file.")
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "model_id": "eleven_turbo_v2",  
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

   

    print("Sending text to ElevenLabs Turbo API...")

    response = requests.post(url, headers=headers, json=payload)




    temp_mp3_path = output_path.replace(".wav", ".mp3")


    if response.status_code == 200:
        # with open(output_path, "wb") as file:
        with open(temp_mp3_path, "wb") as file:

            file.write(response.content)






             # Force proper format conversion after generation
        sound = AudioSegment.from_file(temp_mp3_path)
        sound = sound.set_channels(1).set_sample_width(2)  # Mono, 16-bit
        sound.export(output_path, format="wav")





        print(f"Audio saved to {output_path}")
    else:
        print(f"Error {response.status_code}: {response.text}")

# 🧪 Direct testing mode
if __name__ == "__main__":
    test_text = "The Ocean has many undiscovered species living in it."
    synthesize_speech(test_text)

