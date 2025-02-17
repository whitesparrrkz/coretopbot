import discord
import requests
from utils.list_buttons import ListButtons

def getLevels(pos, level_range):
    url = f"http://localhost:8080/coretop/api/level/getLevelsByRange?position={pos}&length={level_range}"
    victors = []
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        levels = response.json()

        for i in range(pos, pos+len(levels)):
            url = f"http://localhost:8080/coretop/api/victor/getFirstVictorByLevelPosition?position={i}"
            response = requests.get(url)
            if response.status_code != 200:
                raise requests.exceptions.RequestException()
            try:
                response_json = response.json()
                victors.append(response_json["victor_name"])
            except ValueError:
                victors.append("None")
    except requests.exceptions.RequestException as e:
        return [None, None]
    
    return [levels, victors]

def makeEmbed(levels, victors, pos, level_range):
    embed = discord.Embed(title="The CORETOP List", color=discord.Colour.blue())

    embed.add_field(name="Levels:", value="", inline=False)
    if levels != None or victors != None:
        for i in range(0, len(levels)): 
            embed.add_field(name=f"**{str(levels[i]["level_position"])}.** `{levels[i]["level_name"]}` {{T{levels[i]["level_tier"]}}} **-** {levels[i]["level_creator"]}", value=f"*First Victor:* {victors[i]}", inline=False)

    embed.set_footer(text=f"Showing levels {pos}-{pos+level_range-1}")
    return embed

def list_levels():
    level_range = 10
    levels, victors = getLevels(1, level_range)
    return makeEmbed(levels, victors, 1, level_range), ListButtons(level_range, getLevels, makeEmbed)