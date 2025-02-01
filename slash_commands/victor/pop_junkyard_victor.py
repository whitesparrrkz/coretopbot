from dotenv import load_dotenv
import os
import discord
import requests

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

def pop_junkyard_victor(level_name):
    headers = {"token": coretop_Token}
    url = f"http://localhost:8080/coretop/api/victor/popJunkyardVictorByLevelName?level_name={level_name}"

    try:
        response = requests.delete(url, headers=headers)

        if not response.status_code == 200:
            embedFailure = discord.Embed(title="Pop Junkyard Victor Failed", color=discord.Colour.red())
            embedFailure.add_field(name="Level Name", value=level_name)
            return embedFailure
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        
    embed = discord.Embed(
        title="Junkyard Victor Popped",
        color=discord.Colour.green(),
    )
    embed.add_field(name="Level Name", value=level_name, inline=True)
    return embed