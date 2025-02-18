import requests
import yt_dlp
import asyncio

resolutions = ["maxresdefault", "hqdefault", "mqdefault", "sddefault"]

def get_video_thumbnail(video_url):
    video_id = video_url[17:28]

    for resolution in resolutions:
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/{resolution}.jpg"
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            break

    return thumbnail_url

def validate_video_link(video_url):
    if video_url[0:17] == "https://youtu.be/" and len(video_url) >= 28:
        return True
    return False
    

async def validate_trim(video_url: str, start_trim: int, end_trim: int):
    if start_trim < 0 or end_trim < 0:
        return False
    
    try:
        ydl_opts = {
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = await asyncio.to_thread(ydl.extract_info, video_url, download=False)
            video_duration = info_dict.get('duration', None)
    except:
        print("Failed to get duration of video")
        return False
    
    return (start_trim + end_trim) < video_duration
