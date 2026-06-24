import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

# Decode Base64 cookies and write to cookies.txt
if "YOUTUBE_COOKIES_B64" in os.environ:
    try:
        decoded = base64.b64decode(os.environ["YOUTUBE_COOKIES_B64"])
        with open("cookies.txt", "wb") as f:
            f.write(decoded)
        print("cookies.txt written successfully")
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
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "nocheckcertificate": True,
            "cookiefile": "cookies.txt"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        return {"status": "ok", "data": info}

    except Exception as e:
        return {"status": "error", "message": str(e)}
