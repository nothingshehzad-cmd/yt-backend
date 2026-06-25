import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp

# Cookie file ka path
COOKIE_PATH = "cookies.txt"

# Environment variable se cookies ko seedha write karein
if "YOUTUBE_COOKIES_B64" in os.environ:
    try:
        cookies_content = os.environ["YOUTUBE_COOKIES_B64"]
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


# ⭐ NEW: Direct Download Endpoint (Fixes new-tab issue)
@app.get("/download")
def download(video_url: str):
    try:
        # Temporary filename
        filename = f"{uuid.uuid4()}.mp4"

        ydl_opts = {
            "outtmpl": filename,
            "cookiefile": COOKIE_PATH,
            "quiet": True,
            "format": "bestvideo+bestaudio/best"
        }

        # Download file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Return file as attachment
        return FileResponse(
            filename,
            media_type="video/mp4",
            filename="video.mp4"
        )

    except Exception as e:
        return {"status": "error", "message": str(e)}
