from dotenv import load_dotenv
import os
import discord
import requests

load_dotenv()
coretop_Token: str = os.getenv("CORETOP_TOKEN")

tiers = ['t8', 't7', 't6', 't5', 't4', 't3', 't2', 't1', 'insane', 'hard', 'medium', 'easy']

class AddLevelModal(discord.ui.Modal):
    def __init__(self, send_announcement, announcements_id, bot: discord.Bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.send_announcement = send_announcement
        self.announcements_id = announcements_id
        self.bot = bot

        self.add_item(discord.ui.InputText(label="Level Name;Level ID", max_length=35))
        self.add_item(discord.ui.InputText(label="Level Position"))
        self.add_item(discord.ui.InputText(label="Level Creators", max_length=50))
        self.add_item(discord.ui.InputText(label="Level Tier", max_length=20))
        self.add_item(discord.ui.InputText(label="Level Video URL (MUST BE youtu.be)", max_length=80, placeholder="https://youtu.be/"))

    async def callback(self, interaction: discord.Interaction):
        split1 = self.children[0].value.split(';')

        failed = False
        embedFailure = discord.Embed(title="Add Level Failed", color=discord.Colour.red())
        if not self.children[1].value.isdigit() or int(self.children[1].value)<=0:
            failed = True
            embedFailure.add_field(name="Invalid Position", value=self.children[1])
        
        if not split1[1].isdigit() and len(split1[1])>20:
            failed = True
            embedFailure.add_field(name="Invalid ID", value=split1[1])
        
        if not (self.children[3].value).lower() in tiers:
            failed = True
            embedFailure.add_field(name="Invalid Tier", value=self.children[3].value)

        #TODO improve url error handling
        if (self.children[4].value)[0:17] != "https://youtu.be/" or len(self.children[4].value) != 28:
            failed = True
            embedFailure.add_field(name="Invalid Video URL", value=self.children[4].value)

        if failed:
            await interaction.response.send_message(embed=embedFailure)
            return
        
        url = f"http://localhost:8080/coretop/api/level/addLevel"
        data = {
            "level_position": self.children[1].value,
            "level_name": split1[0],
            "level_creator": self.children[2].value,
            "level_id": split1[1],
            "level_tier": (self.children[3].value).lower(),
            "level_video": self.children[4].value
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
        embed.add_field(name="Level Position", value=self.children[1].value)
        embed.add_field(name="Level Creators", value=self.children[2].value)
        embed.add_field(name="Level Tier", value=self.children[3].value)
        embed.add_field(name="Level ID", value=split1[1])
        embed.add_field(name="Level Video URL", value=self.children[4].value)

        await interaction.response.send_message(embed=embed)
        if self.send_announcement:
            channel = self.bot.get_channel(self.announcements_id)
            await channel.send("TEST level added because i gott a finish this latr when more levels")

def add_level(bot, announcements_id, send_announcement):
    return AddLevelModal(title="Add Level", send_announcement=send_announcement, announcements_id=announcements_id, bot=bot)
    