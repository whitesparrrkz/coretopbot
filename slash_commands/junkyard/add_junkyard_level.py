from dotenv import load_dotenv
import os
import discord
import requests
from utils.video_link import validate_video_link

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

def add_junkyard_level(name, tier, video, start_trim, end_trim):
    embedFailure = discord.Embed(title="Add Junkyard Level Failed", color=discord.Colour.red())
    failed = False
    
    if not validate_video_link(video):
        failed = True
        embedFailure.add_field(name="Invalid Video URL", value=video)

    if failed:
        return embedFailure
    
    url = f"http://localhost:8080/coretop/api/level/addJunkyardLevel?name={name}&tier={tier}&video={video}&start_trim={start_trim}&end_trim={end_trim}"
    headers = {"token": coretop_Token}

    try:
        response = requests.post(url, headers=headers)
        if not response.status_code == 200:
            error_info = response.json()
            embedFailure.add_field(name=error_info.get('errorCode', 'No error code'), value=error_info.get('errorMessage', 'No error message'))
            return embedFailure
        embed = discord.Embed(title="Junkyard Level Added", color=discord.Colour.green())
        embed.add_field(name="Level Name", value=name)
        embed.add_field(name="Level Tier", value=tier)
        embed.add_field(name="Level Video URL", value=video)
        embed.add_field(name="Start Trim", value=start_trim)
        embed.add_field(name="End Trim", value=end_trim)
        return embed

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    