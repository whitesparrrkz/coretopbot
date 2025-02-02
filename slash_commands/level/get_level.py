import discord
import requests
import os
from utils.get_video_thumbnail import get_video_thumbnail

def get_level_by_position(level_position: int):
    url = f"http://localhost:8080/coretop/api/level/getLevelByPosition?position={level_position}"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        level = response.json()

        url = f"http://localhost:8080/coretop/api/victor/getVictorsByLevelPosition?position={level["level_position"]}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        victors = response.json()

    except requests.exceptions.RequestException as e:
        return makeEmbedFailure(level_position)
    
    return makeEmbed(level, victors)

def get_level_by_name(level_name: str):
    
    try:
        url = f"http://localhost:8080/coretop/api/level/getLevelByName?name={level_name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        level = response.json()

        url = f"http://localhost:8080/coretop/api/victor/getVictorsByLevelPosition?position={level["level_position"]}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        victors = response.json()

    except requests.exceptions.RequestException as e:
        return makeEmbedFailure(level_name)
    
    return makeEmbed(level, victors)

def get_last_level():
    
    try:
        url = f"http://localhost:8080/coretop/api/level/getLastLevel"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        level = response.json()

        url = f"http://localhost:8080/coretop/api/victor/getVictorsByLevelPosition?position={level["level_position"]}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        victors = response.json()

    except requests.exceptions.RequestException as e:
        return discord.Embed(title="No Levels Exist/No Victors Exist", color=discord.Colour.red())
    
    return makeEmbed(level, victors)

def makeEmbedFailure(s):
    embed = discord.Embed(title="Get Level Failed", color=discord.Colour.red())
    embed.add_field(name="Invalid Position/Name", value=s)

    return embed

def makeEmbed(level, victors):
    embed = discord.Embed(
        title=level["level_name"],
        color=discord.Colour.blue(),
    )

    victorsstr = ""
    i = 1
    for victor in victors:
        victorsstr += f"{i}. {victor["victor_name"]}\n"
        i += 1

    embed.add_field(name="Level Position", value=str(level["level_position"]), inline=True)
    embed.add_field(name="Level Creator(s)", value=level["level_creator"], inline=True)
    embed.add_field(name="Level Tier", value=level["level_tier"], inline=True)
    embed.add_field(name="Level Victors", value=victorsstr, inline=True)
    embed.add_field(name="Level ID", value=level["level_id"], inline=True)
    embed.add_field(name="Video Link", value=level["level_video"], inline=True)
    embed.set_image(url=get_video_thumbnail(level["level_video"]))

    return embed