import discord
import requests

range = 10

class MyView(discord.ui.View):
    def __init__(self, timeout = 180):
        super().__init__()

        self.pos = 1

    @discord.ui.button(style=discord.ButtonStyle.primary, label="<") 
    async def button1_callback(self, button, interaction: discord.Interaction):
        if self.pos-range < 1: 
            await interaction.response.defer()
            return
        self.pos -= range
        await interaction.response.edit_message(embed=makeEmbed(getLevels(self.pos), self.pos))

    @discord.ui.button(style=discord.ButtonStyle.primary, label=">") 
    async def button2_callback(self, button, interaction):
        self.pos += range
        levels = getLevels(self.pos)
        if len(levels) == 0:
            await interaction.response.defer()
            return
        await interaction.response.edit_message(embed=makeEmbed(levels, self.pos))

def getLevels(pos: int):
    url = f"http://localhost:8080/coretop/api/getLevelsByRange?position1={pos}&position2={pos+range-1}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            levels = response.json()

    except requests.exceptions.RequestException as e:
        return None
    return levels

def makeEmbed(levels, pos):
    embed = discord.Embed(title="The CORETOP List", color=discord.Colour.blue())

    values=""

    for level in levels:
        values += f"**{str(level["level_position"])}.** `{level["level_name"]}`\n"

    embed.add_field(name="Levels:", value=values, inline=True)

    embed.set_footer(text=f"Showing levels {pos}-{pos+range-1}")
    return embed

def list_levels():
    return makeEmbed(getLevels(1), 1), MyView()