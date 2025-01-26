import discord
import requests

level_range = 10

class ListButtons(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__()

        self.pos = 1

    @discord.ui.button(style=discord.ButtonStyle.primary, label="<") 
    async def button1_callback(self, button, interaction: discord.Interaction):
        if self.pos-level_range < 1: 
            await interaction.response.defer()
            return
        self.pos -= level_range
        levels, victors = getLevels(self.pos)
        await interaction.response.edit_message(embed=makeEmbed(levels, victors, self.pos))

    @discord.ui.button(style=discord.ButtonStyle.primary, label=">") 
    async def button2_callback(self, button, interaction):
        self.pos += level_range
        levels, victors = getLevels(self.pos)
        if levels == None:
            self.pos -= level_range
            await interaction.response.defer()
            return
        await interaction.response.edit_message(embed=makeEmbed(levels, victors, self.pos))

def getLevels(pos: int):
    url = f"http://localhost:8080/coretop/api/level/getLevelsByRange?position1={pos}&position2={pos+level_range-1}"
    victors = []
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        levels = response.json()

        for i in range(1, len(levels)+1):
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
        return None, None
    
    return levels, victors

def makeEmbed(levels, victors, pos):
    embed = discord.Embed(title="The CORETOP List", color=discord.Colour.blue())

    embed.add_field(name="Levels:", value="", inline=False)
    if levels != None:
        for i in range(0, len(levels)): 
            embed.add_field(name=f"**{str(levels[i]["level_position"])}.** `{levels[i]["level_name"]}` **-** {levels[i]["level_creator"]}", value=f"*First Victor:* {victors[i]}", inline=False)

    embed.set_footer(text=f"Showing levels {pos}-{pos+level_range-1}")
    return embed

def list_levels():
    levels, victors = getLevels(1)
    return makeEmbed(levels, victors, 1), ListButtons()