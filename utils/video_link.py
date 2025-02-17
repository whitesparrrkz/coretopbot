import requests

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
    
