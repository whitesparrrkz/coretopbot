import requests

resolutions = ["maxresdefault", "hqdefault", "mqdefault", "sddefault"]

def get_video_thumbnail(video_url):
    video_id = video_url[17:]

    for resolution in resolutions:
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/{resolution}.jpg"
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            break

    return thumbnail_url
