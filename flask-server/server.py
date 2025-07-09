import os
import sys
import time
import threading
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cv2
import numpy as np
import mss

# Allow imports from parent folder
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))

# Import your existing modules
from recorder import record_audio
from transcriber import transcribe_audio
from tts import synthesize_speech
import audio2face_api as a2f

# Import Claude integration
from claude_integration import get_claude_response

app = Flask(__name__)
CORS(app, origins="*")

# Output directory for all audio files
OUTPUT_DIR = os.path.join(HERE, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
REC_WAV = os.path.join(OUTPUT_DIR, "mic_input.wav")
TTS_WAV = os.path.join(OUTPUT_DIR, "tts_output.wav")

# Global state for real-time updates
pipeline_state = {
    "current_step": 0,
    "status": "idle",
    "transcript": "",
    "claude_response": "",
    "error": None,
    "stream_active": False
}

# Video streaming globals
streaming_active = False
current_frame = None

# Audio2Face capture coordinates
AUDIO2FACE_COORDS = {
    "left": 150,
    "top": 150,
    "width": 800,
    "height": 600
}

def send_progress_update(step, status, data=None):
    """Send real-time progress updates"""
    pipeline_state["current_step"] = step
    pipeline_state["status"] = status
    if data:
        pipeline_state.update(data)
    print(f"📡 Progress Update: Step {step} - {status}")

def capture_audio2face_viewport():
    """Capture Audio2Face viewport"""
    global streaming_active, current_frame
    
    with mss.mss() as sct:
        while streaming_active:
            try:
                monitor = AUDIO2FACE_COORDS.copy()
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
                frame = cv2.resize(frame, (640, 480))
                
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                current_frame = buffer.tobytes()
                
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"❌ Screen capture error: {e}")
                time.sleep(1)

@app.route("/record_and_speak", methods=["POST"])
def record_and_speak():
    """
    Enhanced AI pipeline: Record → Transcribe → Claude AI → TTS → Audio2Face
    """
    global streaming_active
    
    try:
        data = request.get_json() or {}
        duration = float(data.get("duration", 5.0))
        
        if not (0.5 <= duration <= 30):
            return jsonify({"error": "Duration must be between 0.5-30 seconds"}), 400

        # Reset state
        pipeline_state.update({
            "current_step": 0,
            "status": "starting",
            "transcript": "",
            "claude_response": "",
            "error": None,
            "stream_active": False
        })

        print(f"🎤 Starting {duration}s recording...")
        send_progress_update(1, "recording")
        
        # Step 1: Record from microphone
        # record_audio(REC_WAV, duration)
        # print("✅ Recording complete")
        # send_progress_update(1, "complete")

        
        record_audio(REC_WAV, int(duration))
        print("✅ Recording complete")
        send_progress_update(1, "complete")


        # Step 2: Transcribe the recorded audio
        print("🔤 Transcribing audio...")
        send_progress_update(2, "processing")
        user_text = transcribe_audio(REC_WAV).strip()
        
        if not user_text:
            pipeline_state["error"] = "Transcription failed - no text detected"
            return jsonify({"error": "Transcription failed - no text detected"}), 500
        
        print(f"✅ User said: '{user_text}'")
        send_progress_update(2, "complete", {"transcript": user_text})

        # Step 3: Get Claude AI response
        print("🤖 Getting Claude AI response...")
        send_progress_update(3, "thinking")
        claude_response = get_claude_response(user_text)
        
        if not claude_response:
            claude_response = "I'm sorry, I didn't understand that."
        
        print(f"✅ Claude responds: '{claude_response}'")
        send_progress_update(3, "complete", {"claude_response": claude_response})

        # Step 4: Generate TTS from Claude's response (not user's text!)
        print("🗣️ Generating TTS for Claude's response...")
        send_progress_update(4, "generating")
        synthesize_speech(claude_response, TTS_WAV)  # Use Claude's response
        print("✅ TTS generation complete")
        send_progress_update(4, "complete")

        # Step 5: Audio2Face lip-sync animation
        print("🎭 Starting Audio2Face animation...")
        send_progress_update(5, "animating")
        
        try:
            # Load USD scene
            a2f.load_usd(r"C:\Users\Devan\Desktop\Working Face.usd")
            
            # Get player instances
            players = a2f.get_player_instances()
            if not players:
                print("⚠️ No Audio2Face Player found in scene")
                send_progress_update(5, "error", {"error": "No Audio2Face Player found"})
                return jsonify({
                    "success": False,
                    "error": "No Audio2Face Player found in scene"
                }), 500
            
            player = players[0]
            print(f"🎬 Using player: {player}")

            # Configure audio playback
            a2f.set_root_path(OUTPUT_DIR, player=player)
            a2f.set_track(os.path.basename(TTS_WAV), player=player, time_range=[0, -1])
            a2f.set_range(player=player, time_range=[0, -1])
            
            # Start video streaming
            streaming_active = True
            threading.Thread(target=capture_audio2face_viewport, daemon=True).start()
            
            # Small delay then play
            time.sleep(0.3)
            a2f.play_audio(player=player)
            
            print("✅ Magic Mirror is speaking Claude's response!")
            send_progress_update(5, "complete", {"stream_active": True})
            
            return jsonify({
                "success": True,
                "user_transcript": user_text,
                "claude_response": claude_response,
                "tts_file": TTS_WAV,
                "duration_recorded": duration,
                "message": "AI conversation complete!",
                "stream_active": True
            })
            
        except Exception as a2f_error:
            print(f"❌ Audio2Face error: {str(a2f_error)}")
            send_progress_update(5, "error", {"error": str(a2f_error)})
            return jsonify({"error": f"Audio2Face failed: {str(a2f_error)}"}), 500

    except Exception as e:
        print(f"❌ Error in AI pipeline: {str(e)}")
        pipeline_state["error"] = str(e)
        return jsonify({"error": f"AI pipeline failed: {str(e)}"}), 500

@app.route("/progress", methods=["GET"])
def get_progress():
    """Get current pipeline progress"""
    return jsonify(pipeline_state)

@app.route("/stream/start", methods=["POST"])
def start_stream():
    """Start video stream"""
    global streaming_active
    
    if not streaming_active:
        streaming_active = True
        threading.Thread(target=capture_audio2face_viewport, daemon=True).start()
        print("📹 Video stream started")
    
    return jsonify({"success": True, "streaming": streaming_active})

@app.route("/stream/stop", methods=["POST"])
def stop_stream():
    """Stop video stream"""
    global streaming_active
    streaming_active = False
    print("⏹️ Video stream stopped")
    return jsonify({"success": True, "streaming": streaming_active})

@app.route("/video_feed")
def video_feed():
    """Video streaming endpoint"""
    def generate_frames():
        while streaming_active:
            if current_frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + current_frame + b'\r\n')
            time.sleep(0.033)
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/health", methods=["GET"])
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "ai_enabled": True,
        "claude_available": True,
        "streaming_active": streaming_active
    })

if __name__ == "__main__":
    print("🚀 Starting Magic Mirror AI Server with Claude Integration")
    print("🤖 Claude AI: Ready for conversations")
    print("🎭 Audio2Face: Ready for responses")
    print("📹 Video streaming: Ready")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
