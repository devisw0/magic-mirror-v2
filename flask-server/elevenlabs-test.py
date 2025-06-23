import socket

try:
    ip = socket.gethostbyname("api.elevenlabs.io")
    print("Resolved IP:", ip)
except Exception as e:
    print("DNS failed:", e)
