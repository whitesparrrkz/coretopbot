from dotenv import load_dotenv
import os
import discord
import requests
import json

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

class AddLevelModalFirst(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Level Name;Level ID"))
        self.add_item(discord.ui.InputText(label="Level Position;Level First Victor"))
        self.add_item(discord.ui.InputText(label="Level Creators"))
        self.add_item(discord.ui.InputText(label="Level Tier"))
        self.add_item(discord.ui.InputText(label="Level Video URL"))

    async def callback(self, interaction: discord.Interaction):
        split1 = self.children[0].value.split(';')
        split2 = self.children[1].value.split(';')

        failed = False
        embedFailure = discord.Embed(title="Add Level Failed", color=discord.Colour.red())
        if not split2[0].isdigit():
            failed = True
            embedFailure.add_field(name="Invalid Position", value=split1[1])
        
        if not split1[1].isdigit() and len(split1[1])>20:
            failed = True
            embedFailure.add_field(name="Invalid ID", value=split1[1])
        
        if failed:
            await interaction.response.send_message(embed=embedFailure)
            return
        
        url = f"http://localhost:8080/coretop/api/addLevel"
        data = {
            "level_position": int(split2[0]),
            "level_name": split1[0],
            "level_first_victor": split2[1],
            "level_creator": self.children[2].value,
            "level_id": split1[1],
            "level_tier": self.children[3].value,
            "level_video": self.children[4].value
        }

        headers = {"token": coretop_Token}

        try:
            response = requests.post(url, json=data, headers=headers)
            if not response.status_code == 200:
                print('Error:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

        embed = discord.Embed(title="Level Added", color=discord.Colour.green())
        embed.add_field(name="Level Name", value=split1[0])
        embed.add_field(name="Level Position", value=split2[0])
        embed.add_field(name="Level First Victor", value=split2[1])
        embed.add_field(name="Level Creators", value=self.children[2].value)
        embed.add_field(name="Level Tier", value=self.children[3].value)
        embed.add_field(name="Level ID", value=split1[1])
        embed.add_field(name="Level Video URL", value=self.children[4].value)

        await interaction.response.send_message(embed=embed)

def add_level():
    return AddLevelModalFirst(title="Add Level")