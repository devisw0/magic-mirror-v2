# audio2face_api.py

import requests

A2F_API_URL = "http://localhost:8011"

def load_usd(file_path: str) -> dict:
    url = f"{A2F_API_URL}/A2F/USD/Load"
    resp = requests.post(url, json={"file_name": file_path})
    resp.raise_for_status()
    return resp.json()

def get_player_instances() -> list[str]:
    """
    GET /A2F/Player/GetInstances
    Returns a flat list of all audio-player prim paths in the stage.
    """
    url = f"{A2F_API_URL}/A2F/Player/GetInstances"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    # new API returns data["result"] = {"regular": [...], "streaming": [...]}
    result = data.get("result", {})
    if isinstance(result, dict):
        regular   = result.get("regular", [])
        streaming = result.get("streaming", [])
        return regular + streaming

    # fallback: maybe it’s already a list
    if isinstance(result, list):
        return result

    return []


def set_root_path(path: str, player: str) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/SetRootPath"
    resp = requests.post(url, json={"a2f_player": player, "dir_path": path})
    resp.raise_for_status()
    return resp.json()

def set_track(
    file_name: str,
    player: str,
    time_range: list[int] | None = None
) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/SetTrack"
    payload = {"a2f_player": player, "file_name": file_name}
    if time_range is not None:
        payload["time_range"] = time_range
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def play_audio(player: str) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/Play"
    resp = requests.post(url, json={"a2f_player": player})
    resp.raise_for_status()
    return resp.json()

def generate_emotion_keys(
    instance: str,
    window_size: int = 8,
    stride: int = 4,
    emotion_strength: float = 0.8
) -> dict:
    url = f"{A2F_API_URL}/A2F/A2E/GenerateKeys"
    payload = {
        "a2f_instance": instance,
        "a2e_window_size": window_size,
        "a2e_stride": stride,
        "a2e_emotion_strength": emotion_strength
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def export_geometry_cache(
    meshes: list[str],
    export_directory: str,
    file_name: str,
    cache_type: str = "usd",
    xform_keys: bool = True,
    batch: bool = False,
    fps: int = 24
) -> dict:
    url = f"{A2F_API_URL}/A2F/Exporter/ExportGeometryCache"
    payload = {
        "meshes": meshes,
        "export_directory": export_directory,
        "file_name": file_name,
        "cache_type": cache_type,
        "xform_keys": xform_keys,
        "batch": batch,
        "fps": fps
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def get_root_path(player: str) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/GetRootPath"
    resp = requests.post(url, json={"a2f_player": player})
    resp.raise_for_status()
    return resp.json()

def get_tracks(player: str) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/GetTracks"
    resp = requests.post(url, json={"a2f_player": player})
    resp.raise_for_status()
    return resp.json()

def get_current_track(player: str) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/GetCurrentTrack"
    resp = requests.post(url, json={"a2f_player": player})
    resp.raise_for_status()
    return resp.json()

def get_time(player: str) -> dict:
    url = f"{A2F_API_URL}/A2F/Player/GetTime"
    resp = requests.post(url, json={"a2f_player": player})
    resp.raise_for_status()
    return resp.json()

# ─── NEW: explicitly set & get play range ───

def set_range(player: str, time_range: list[int]) -> dict:
    """
    POST /A2F/Player/SetRange
    Body: { "a2f_player": "<player>", "time_range": [start, end] }
    """
    url = f"{A2F_API_URL}/A2F/Player/SetRange"
    payload = {"a2f_player": player, "time_range": time_range}
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

def get_range(player: str) -> dict:
    """
    POST /A2F/Player/GetRange
    Body: { "a2f_player": "<player>" }
    """
    url = f"{A2F_API_URL}/A2F/Player/GetRange"
    resp = requests.post(url, json={"a2f_player": player})
    resp.raise_for_status()
    return resp.json()
