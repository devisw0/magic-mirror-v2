import requests
import json

def test_complete_pipeline():
    """Test the complete record → transcribe → TTS → Audio2Face pipeline"""
    
    url = "http://127.0.0.1:5000/record_and_speak"
    payload = {"duration": 7}  # Record for 7 seconds
    
    print("🎤 Sending request to record and process audio...")
    print(f"📡 URL: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=60)  # Longer timeout for processing
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"🔤 Transcript: '{result.get('transcript')}'")
            print(f"🎵 TTS File: {result.get('tts_file')}")
            print(f"⏱️ Duration: {result.get('duration_recorded')}s")
            print(f"💬 Message: {result.get('message')}")
        else:
            print("❌ ERROR!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_health():
    """Test the health endpoint"""
    url = "http://127.0.0.1:5000/health"
    
    try:
        response = requests.get(url)
        print(f"🏥 Health Check: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Audio Pipeline Server\n")
    
    # Test health first
    test_health()
    print("\n" + "="*50 + "\n")
    
    # Test complete pipeline
    test_complete_pipeline()
