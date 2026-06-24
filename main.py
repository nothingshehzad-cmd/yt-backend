import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

# Cookie file ka path
COOKIE_PATH = "cookies.txt"

# Environment variable se cookies ko seedha write karein
if "YOUTUBE_COOKIES_B64" in os.environ:
    try:
        # Pura cookies ka text read karein
        cookies_content = os.environ["YOUTUBE_COOKIES_B64"]
        
        # File mein save karein (encoding="utf-8" zaroori hai)
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            f.write(cookies_content)
        print("cookies.txt successfully created from environment variable.")
    except Exception as e:
        print(f"Error creating cookies file: {e}")

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
    # Check karein ki cookies file exist karti hai
    if not os.path.exists(COOKIE_PATH):
        return {"status": "error", "message": "cookies.txt file not found"}

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "nocheckcertificate": True,
            "cookiefile": COOKIE_PATH
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {"status": "ok", "data": info}

    except Exception as e:
        return {"status": "error", "message": str(e)}
