import discord
import requests
from utils.get_video_thumbnail import get_video_thumbnail

def get_level_by_position(level_position: int):
    url = f"http://localhost:8080/coretop/api/getLevelByPosition?position={level_position}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            level = response.json()
            
    except requests.exceptions.RequestException as e:
        return makeEmbedFailure(level_position)
    
    return makeEmbed(level)

def get_level_by_name(level_name: str):
    url = f"http://localhost:8080/coretop/api/getLevelByName?name={level_name}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            level = response.json()

    except requests.exceptions.RequestException as e:
        return makeEmbedFailure(level_name)
    
    return makeEmbed(level)

def makeEmbedFailure(s):
    embed = discord.Embed(title="Get Level Failed", color=discord.Colour.red())
    embed.add_field(name="Invalid Position/Name", value=s)

    return embed

def makeEmbed(level):
    embed = discord.Embed(
        title=level["level_name"],
        color=discord.Colour.blue(),
    )

    embed.add_field(name="Level Position", value=str(level["level_position"]), inline=True)
    embed.add_field(name="Level Creator(s)", value=level["level_creator"], inline=True)
    embed.add_field(name="Level Tier", value=level["level_tier"], inline=True)
    embed.add_field(name="Level ID", value=level["level_id"], inline=True)
    embed.set_image(url=get_video_thumbnail(level["level_video"]))
    return embed