import discord
import requests
import os
from collections import OrderedDict

from utils.tiers import get_tiers
from utils.get_discord_file import get_tier_png
# possibly change to async http here as a lot of http requests are being called

tiers = OrderedDict(reversed(list((get_tiers()).items())))

def get_victor(name):

    url = f"http://localhost:8080/coretop/api/level/getPlayerTopLevels?player={name}&num=5"
    embedFailure = discord.Embed(title="Get Victor Failed", color=discord.Colour.red())
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        levels = response.json()
        if len(levels) == 0:
            raise requests.exceptions.RequestException()
    except:
        embedFailure.add_field(name="Top Levels", value=f"Failed to get top levels of **( {name} )**")
        return embedFailure
    
    points = 0
    tier_count: dict = {}
    for tier in tiers:
        tier_count[tier] = 0

    for tier in tiers:
        url = f"http://localhost:8080/coretop/api/level/getNumOfTiersByPlayer?player={name}&tier={tier}"
        try:
            response = requests.get(url)

            if response.status_code != 200:
                raise requests.exceptions.RequestException()
            count = response.json()
            tier_count[tier] = count
            points += count * tiers[tier]
        except:
            embedFailure.add_field(name="Top Levels", value=f"Failed to get top levels of {name}")
            return embedFailure

    embed = discord.Embed(title=name, color=discord.Colour.blue())
    embed.add_field(name="Hardest Level", value=f"**1.** `{levels[0]["level_name"]}` ({levels[0]["level_tier"]})", inline=False)

    othersstr = ""
    for i in range(1,len(levels)):
        othersstr += f"**{i+1}.** `{levels[i]["level_name"]}` ({levels[i]["level_tier"]})\n"
    embed.add_field(name="Other Levels", value=othersstr, inline=True)

    embed.add_field(name="List Points", value=str(points))

    tiersstr = ""
    for tier in tier_count:
        if(tier_count[tier] != 0):
            tiersstr += f"**{tier}:** `{tier_count[tier]}`\n"
    embed.add_field(name="Tier Stats", value=tiersstr, inline=False)

    file = get_tier_png(levels[0]["level_tier"])
    
    embed.set_thumbnail(url="attachment://" + file.filename)

    return embed, file