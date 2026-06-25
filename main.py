import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import yt_dlp

COOKIE_PATH = "cookies.txt"

# Cookie setup
if "YOUTUBE_COOKIES_B64" in os.environ:
    try:
        with open(COOKIE_PATH, "w", encoding="utf-8") as f:
            f.write(os.environ["YOUTUBE_COOKIES_B64"])
    except Exception as e:
        print(f"Error: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# NAYA APPROACH: Redirect to Direct URL (Faster & No Timeout)
@app.get("/download")
async def download(video_url: str):
    # Hum video download nahi karenge, balki user ko direct file link par bhej denge
    # Isse server par load nahi padega aur timeout nahi hoga
    return RedirectResponse(url=video_url)
