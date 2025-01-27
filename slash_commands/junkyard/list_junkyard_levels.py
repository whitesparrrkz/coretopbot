import discord
import requests

level_range = 10

conv_dif = {
    "medium": "Medium Demon",
    "easy": "Easy Demon"
}

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
        levels = getLevels(self.pos)
        await interaction.response.edit_message(embed=makeEmbed(levels, self.pos))

    @discord.ui.button(style=discord.ButtonStyle.primary, label=">") 
    async def button2_callback(self, button, interaction):
        self.pos += level_range
        levels = getLevels(self.pos)
        if levels == None:
            self.pos -= level_range
            await interaction.response.defer()
            return
        await interaction.response.edit_message(embed=makeEmbed(levels, self.pos))

def getLevels(pos: int):
    url = f"http://localhost:8080/coretop/api/level/getJunkyardLevelsByRange?position={pos}&len={pos+level_range-1}"
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        levels = response.json()

    except requests.exceptions.RequestException as e:
        return None
    
    return levels

def makeEmbed(levels, pos):
    embed = discord.Embed(title="The CORETOP Junkyard List", color=discord.Colour.blue())
    levelstr = ""
    if levels != None:
        for level in levels: 
            levelstr += f"`{level["level_name"]}` - {conv_dif[level["level_tier"]]}\n"
    embed.add_field(name="Levels:", value=levelstr, inline=False)


    embed.set_footer(text=f"Showing levels {pos}-{pos+level_range-1}")
    return embed

def list_junkyard_levels():
    levels = getLevels(1)
    return makeEmbed(levels, 1), ListButtons()