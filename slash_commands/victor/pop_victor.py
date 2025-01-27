from dotenv import load_dotenv
import os
import discord
import requests

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

def pop_victor(level_position):
    headers = {"token": coretop_Token}
    url = f"http://localhost:8080/coretop/api/victor/popVictorByLevelPosition?position={level_position}"

    try:
        response = requests.delete(url, headers=headers)

        if not response.status_code == 200:
            embedFailure = discord.Embed(title="Pop Victor Failed", color=discord.Colour.red())
            embedFailure.add_field(name="Level Position", value=level_position)
            return embedFailure
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        
    embed = discord.Embed(
        title="Victor Popped",
        color=discord.Colour.green(),
    )
    embed.add_field(name="Level Position", value=level_position, inline=True)
    return embed