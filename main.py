from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

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
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return {"status": "ok", "data": info}

    except Exception as e:
        return {"status": "error", "message": str(e)}
