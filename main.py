import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

# Cookie file ka absolute path set karein
COOKIE_PATH = os.path.join(os.getcwd(), "cookies.txt")

# Decode Base64 cookies and write to cookies.txt (Robust version)
if "YOUTUBE_COOKIES_B64" in os.environ:
    try:
        # Extra spaces/newlines remove karein
        b64_str = os.environ["YOUTUBE_COOKIES_B64"].strip()
        decoded = base64.b64decode(b64_str)
        
        # Binary write mode mein save karein
        with open(COOKIE_PATH, "wb") as f:
            f.write(decoded)
        print(f"cookies.txt written successfully at {COOKIE_PATH}")
    except Exception as e:
        print("Failed to decode cookies:", e)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/extract")
def extract(url: str):
    # Check karein ki cookies file exist karti hai ya nahi
    if not os.path.exists(COOKIE_PATH):
        return {"status": "error", "message": "cookies.txt not found"}

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "nocheckcertificate": True,
            "cookiefile": COOKIE_PATH, # Absolute path use karein
            "cachedir": False          # Caching issue se bachne ke liye
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {"status": "ok", "data": info}

    except Exception as e:
        return {"status": "error", "message": str(e)}
