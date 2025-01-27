from dotenv import load_dotenv
import os
import discord
import requests

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

tiers = ['medium', 'easy']

def add_junkyard_level(name, tier, video):
    embedFailure = discord.Embed(title="Add Junkyard Level Failed", color=discord.Colour.red())
    failed = False

    if not tier in tiers:
        failed = True
        embedFailure.add_field(name="Invalid tier", value=tier)
    
    if video[0:17] != "https://youtu.be/":
        failed = True
        embedFailure.add_field(name="Invalid Video URL", value=video)

    if failed:
        return embedFailure
    
    url = f"http://localhost:8080/coretop/api/level/addJunkyardLevel?name={name}&tier={tier}&video={video}"
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
        return embed

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    