from dotenv import load_dotenv
import os
import discord
import requests

from utils.tiers import get_tiers
from utils.video_stuff import validate_video_link, validate_trim

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

tiers = get_tiers()
tiers = tiers.keys()

class AddLevelModal(discord.ui.Modal):
    def __init__(self, send_announcement, announcements_id, bot: discord.Bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.send_announcement = send_announcement
        self.announcements_id = announcements_id
        self.bot = bot

        self.add_item(discord.ui.InputText(label="Level Name;Level ID", max_length=35))
        self.add_item(discord.ui.InputText(label="Level Position;Level Tier"))
        self.add_item(discord.ui.InputText(label="Level Creators", max_length=50))
        self.add_item(discord.ui.InputText(label="Start Trim;End Trim"))
        self.add_item(discord.ui.InputText(label="Level Video URL (MUST BE youtu.be)", max_length=80, placeholder="https://youtu.be/"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        split1 = self.children[0].value.split(';')
        split2 = self.children[1].value.split(';')
        split3 = self.children[3].value.split(';')
        failed = False
        embedFailure = discord.Embed(title="Add Level Failed", color=discord.Colour.red())
        if not split2[0].isdigit() or int(split2[0])<=0:
            failed = True
            embedFailure.add_field(name="Invalid Position", value=split2[0])
        
        if not split1[1].isdigit() and len(split1[1])>20:
            failed = True
            embedFailure.add_field(name="Invalid ID", value=split1[1])
        
        if not int(split2[1]) in tiers:
            failed = True
            embedFailure.add_field(name="Invalid Tier", value=split2[1])

        if not validate_video_link(self.children[4].value):
            failed = True
            embedFailure.add_field(name="Invalid Video URL", value=self.children[4].value)
            
        #validate_trim() function from video_stuff too overkill for a coretop admin command
        if int(split3[0]) < 0 or int(split3[1]) < 0 or split3[0].isdigit() or split3[1].isdigit():
            failed = True
            embedFailure.add_field(name="Invalid trim (negative)", value=f"(start_trim={split3[0]},end_trim={split3[1]})")

        if failed:
            await interaction.followup.send(embed=embedFailure)
            return
        
        url = f"http://localhost:8080/coretop/api/level/addLevel"
        data = {
            "level_position": split2[0],
            "level_name": split1[0],
            "level_creator": self.children[2].value,
            "level_id": split1[1],
            "level_tier": split2[1],
            "level_video": self.children[4].value,
            "start_trim": split3[0],
            "end_trim": split3[1]
        }

        headers = {"token": coretop_Token}

        try:
            response = requests.post(url, json=data, headers=headers)
            if not response.status_code == 200:
                error_info = response.json()
                embedFailure.add_field(name=error_info.get('errorCode', 'No error code'), value=error_info.get('errorMessage', 'No error message'))
                await interaction.response.send_message(embed=embedFailure)
                return

        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return None

        embed = discord.Embed(title="Level Added", color=discord.Colour.green())
        embed.add_field(name="Level Name", value=split1[0])
        embed.add_field(name="Level Position", value=split2[0])
        embed.add_field(name="Level Creators", value=self.children[2].value)
        embed.add_field(name="Level Tier", value=split2[1])
        embed.add_field(name="Level ID", value=split1[1])
        embed.add_field(name="Level Video URL", value=self.children[4].value)
        embed.add_field(name="Start Trim", value=split3[0])
        embed.add_field(name="End Trim", value=split3[1])

        await interaction.followup.send(embed=embed)
        if self.send_announcement:
            channel = self.bot.get_channel(self.announcements_id)
            await channel.send("TEST level added because i gott a finish this latr when more levels")

def add_level(bot, announcements_id, send_announcement):
    return AddLevelModal(title="Add Level", send_announcement=send_announcement, announcements_id=announcements_id, bot=bot)
    