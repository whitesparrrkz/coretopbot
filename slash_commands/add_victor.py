from dotenv import load_dotenv
import os
import discord
import requests

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

def add_victor(victor_name, level_position):
    url = f"http://localhost:8080/coretop/api/victor/addVictorByLevelPosition?victorName={victor_name}&levelPosition={level_position}"
    headers = {"token": coretop_Token}

    try:
        response = requests.post(url, headers=headers)
        if not response.status_code == 200:
            error_info = response.json()
            embedFailure = discord.Embed(title="Add Victor Failed", color=discord.Colour.red())
            embedFailure.add_field(name=error_info.get('errorCode', 'No error code'), value=error_info.get('errorMessage', 'No error message'))
            return embedFailure

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

    embed = discord.Embed(title="Victor Added", color=discord.Colour.green())
    embed.add_field(name="Victor Name", value=victor_name)
    embed.add_field(name="Level Position", value=level_position)

    return embed