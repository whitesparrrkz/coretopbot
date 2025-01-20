import discord
import requests
from utils.get_video_thumbnail import get_video_thumbnail

def get_level_by_id(level_position: int):
    url = f"http://localhost:8080/coretop/api/getLevelByPosition?position={level_position}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            level = response.json()
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
    return makeEmbed(level)

def get_level_by_name(level_name: str):
    url = f"http://localhost:8080/coretop/api/getLevelByName?name={level_name}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            level = response.json()
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
    return makeEmbed(level)


def makeEmbed(level):
    embed = discord.Embed(
        title=level["level_name"],
        color=discord.Colour.red(),
    )

    embed.add_field(name="Level Position", value=str(level["level_position"]), inline=True)
    embed.add_field(name="Level Creator(s)", value=level["level_creator"], inline=True)
    embed.add_field(name="Level ID", value=level["level_id"], inline=True)
    embed.set_image(url=get_video_thumbnail(level["level_video"]))
    return embed