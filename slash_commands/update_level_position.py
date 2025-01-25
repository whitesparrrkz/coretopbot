from dotenv import load_dotenv
import os
import discord
import requests

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

def update_level_position(old_pos, new_pos):
    headers = {"token": coretop_Token}
    url = f"http://localhost:8080/coretop/api/updateLevelPosition?old_position={old_pos}&new_position={new_pos}"

    try:
        response = requests.put(url, headers=headers)
        if not response.status_code == 200:
            error_info = response.json()
            embedFailure = discord.Embed(title="Update Level Position Failed", color=discord.Colour.red())
            embedFailure.add_field(name=error_info.get('errorCode', 'No error code'), value=error_info.get('errorMessage', 'No error message'))
            return embedFailure
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        
    embed = discord.Embed(
        title="Updated Positions",
        color=discord.Colour.green(),
    )
    embed.add_field(name="Changed:", value=f"Old Position ({old_pos}) -> ({new_pos})", inline=True)
    return embed