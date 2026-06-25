import os
import yt_dlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/extract")
def extract(url: str):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": "in_playlist", # Playlist handle karne ke liye
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {"status": "ok", "data": info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/download")
async def download(video_url: str):
    # Direct streaming URL par bhej dega, browser download shuru kar dega
    return RedirectResponse(url=video_url)
