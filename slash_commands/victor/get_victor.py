import discord
import requests
import os

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
    
    tiers = {
        "t8": 0, "t7": 0, "t6": 0, "t5": 0, "t4": 0, "t3": 0,
        "t2": 0, "t1": 0, "insane": 0, "hard": 0, "medium": 0, "easy": 0,
    }

    for tier in tiers:
        url = f"http://localhost:8080/coretop/api/level/getNumOfTiersByPlayer?player={name}&tier={tier}"
        try:
            response = requests.get(url)

            if response.status_code != 200:
                raise requests.exceptions.RequestException()
            count = response.json()
            tiers[tier] = count
        except:
            embedFailure.add_field(name="Top Levels", value=f"Failed to get top levels of {name}")
            return embedFailure

    embed = discord.Embed(title=name, color=discord.Colour.blue())
    embed.add_field(name="Hardest Level", value=f"**1.** `{levels[0]["level_name"]}` ({levels[0]["level_tier"]})", inline=False)

    othersstr = ""
    for i in range(1,len(levels)):
        othersstr += f"**{i}.** `{levels[i]["level_name"]}` ({levels[i]["level_tier"]})\n"
    embed.add_field(name="Other Levels", value=othersstr, inline=True)

    tiersstr = ""
    for tier in tiers:
        if(tiers[tier] != 0):
            tiersstr += f"**{tier.upper()}:** `{tiers[tier]}`\n"
    embed.add_field(name="Tier Stats", value=tiersstr, inline=True)

    project_root = os.path.dirname(os.path.abspath(__file__)) 
    image_path = os.path.join(project_root, '../../resources/tiers', f"{levels[0]['level_tier']}.png")
    with open(image_path, 'rb') as img:
        file = discord.File(img, filename=f"{levels[0]['level_tier']}.png")
        embed.set_thumbnail(url="attachment://" + file.filename)

    return embed, file