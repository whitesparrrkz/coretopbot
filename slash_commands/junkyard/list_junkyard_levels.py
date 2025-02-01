import discord
import requests

from utils.list_buttons import ListButtons

conv_dif = {
    "medium": "Medium Demon",
    "easy": "Easy Demon"
}

def getLevels(pos, level_range):
    url = f"http://localhost:8080/coretop/api/level/getJunkyardLevelsByRange?position={pos}&length={level_range}"
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        levels = response.json()

    except requests.exceptions.RequestException as e:
        return [None]
    
    return [levels]

def makeEmbed(levels, pos, level_range):
    embed = discord.Embed(title="The CORETOP Junkyard List", color=discord.Colour.blue())
    levelstr = ""

    if levels != None:
        for level in levels: 
            levelstr += f"`{level["level_name"]}` - {conv_dif[level["level_tier"]]}\n"

    embed.add_field(name="Levels:", value=levelstr, inline=False)
    embed.set_footer(text=f"Showing levels {pos}-{pos+level_range-1}")
    return embed

def list_junkyard_levels():
    level_range = 10
    levels = getLevels(1, level_range)
    return makeEmbed(*levels, 1, level_range), ListButtons(level_range, getLevels, makeEmbed)