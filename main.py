import os
import uuid
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp

# Cookie file ka path
COOKIE_PATH = "cookies.txt"

# Environment variable check
if "YOUTUBE_COOKIES_B64" in os.environ:
    try:
        cookies_content = os.environ["YOUTUBE_COOKIES_B64"]
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            f.write(cookies_content)
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

# File cleanup function
def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

@app.get("/extract")
def extract(url: str):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "cookiefile": COOKIE_PATH if os.path.exists(COOKIE_PATH) else None
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {"status": "ok", "data": info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/download")
async def download(video_url: str, background_tasks: BackgroundTasks):
    try:
        file_id = str(uuid.uuid4())
        filename = f"{file_id}.mp4"
        
        ydl_opts = {
            "outtmpl": filename,
            "cookiefile": COOKIE_PATH if os.path.exists(COOKIE_PATH) else None,
            "quiet": True,
            # 'best' format chunne se download speed behtar rahegi
            "format": "best[ext=mp4]/best"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Background task se file delete karwain takay disk space free rahe
        background_tasks.add_task(delete_file, filename)
        
        return FileResponse(
            path=filename,
            media_type="video/mp4",
            filename="video.mp4"
        )
    except Exception as e:
        return {"status": "error", "message": str(e)}
