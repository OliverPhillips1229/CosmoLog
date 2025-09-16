import os
import requests
from django.conf import settings

BASE = "https://api.nasa.gov/mars-photos/api/v1"

def _key():
    return getattr(settings, "NASA_API_KEY", os.getenv("NASA_API_KEY", "DEMO_KEY"))

def get_manifest(rover: str):
    url = f"{BASE}/manifests/{rover.lower()}"
    r = requests.get(url, params={"api_key": _key()}, timeout=15)
    r.raise_for_status()
    return r.json().get("photo_manifest", {})

def get_photos(rover: str, *, sol: int|None=None, earth_date: str|None=None,
               camera: str|None=None, page: int=1):
    assert sol or earth_date, "Provide either sol or earth_date"
    params = {"api_key": _key(), "page": page}
    if sol is not None: params["sol"] = sol
    if earth_date is not None: params["earth_date"] = earth_date
    if camera: params["camera"] = camera.lower()
    url = f"{BASE}/rovers/{rover.lower()}/photos"
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("photos", [])
