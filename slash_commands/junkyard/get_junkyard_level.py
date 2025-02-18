import discord
import requests
from utils.video_stuff import get_video_thumbnail

def get_junkyard_level(level_name: str):
    try:
        url = f"http://localhost:8080/coretop/api/level/getJunkyardLevelByName?name={level_name}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        level = response.json()

        url = f"http://localhost:8080/coretop/api/victor/getJunkyardVictorsByLevelName?level_name={level["level_name"]}"
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        victors = response.json()

    except requests.exceptions.RequestException as e:
        return makeEmbedFailure(level_name)
    
    return makeEmbed(level, victors)

def makeEmbedFailure(s):
    embed = discord.Embed(title="Get Junkyard Level Failed", color=discord.Colour.red())
    embed.add_field(name="Invalid Name", value=s)

    return embed

def makeEmbed(level, victors):
    embed = discord.Embed(
        title=f"Junkyard Level: {level["level_name"]}",
        color=discord.Colour.blue(),
    )

    victorsstr = ""
    i = 1
    for victor in victors:
        victorsstr += f"{i}. {victor["victor_name"]}\n"
        i += 1
    embed.add_field(name="Level Tier", value=level["level_tier"], inline=True)
    embed.add_field(name="Video Link", value=f"{level["level_video"]} (start_trim={level["start_trim"]},end_trim={level["end_trim"]})", inline=True)
    embed.add_field(name="Level Victors", value=victorsstr, inline=False)
    embed.set_image(url=get_video_thumbnail(level["level_video"]))

    return embed