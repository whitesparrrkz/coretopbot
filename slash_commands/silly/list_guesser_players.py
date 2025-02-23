import discord
import requests

from utils.list_buttons import ListButtons

def get_guesser_players(pos, player_range):
    url = f"http://localhost:8080/coretop/api/guesserPlayer/getGuesserPlayersByRange?position={pos}&length={player_range}"
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        players = response.json()
    except requests.exceptions.RequestException as e:
        return [None]
    return [players]

async def make_embed(players, pos, level_range, bot: discord.Bot):
    embed = discord.Embed(title="Guesser Player List", color=discord.Colour.blue())
    playerstr = ""

    if players != None:
        for i in range(0, len(players)): 
            try:
                user = await bot.fetch_user(int(players[i]["user_id"]))
            except:
                continue
            playerstr += f"**{pos+i}.** {user.name}\nTotal Points: **{players[i]["points"]}**\n"

    embed.add_field(name="Players:", value=playerstr, inline=False)
    embed.set_footer(text=f"Showing players {pos}-{pos+level_range-1}")
    return embed

async def list_guesser_players(ctx: discord.ApplicationContext, bot: discord.Bot):
    await ctx.defer()
    embed = await make_embed(*get_guesser_players(1,5), 1, 5, bot)
    await ctx.respond(embed=embed, view=ListButtons(5, get_guesser_players, make_embed, bot))

# this one is different than the one in util, calls make_embed asynchronously
class ListButtons(discord.ui.View):
    def __init__(self, level_range, get_info, make_embed, bot: discord.Bot = None, timeout = 180):
        super().__init__()

        self.pos = 1
        self.level_range = level_range
        self.get_info = get_info
        self.make_embed = make_embed
        self.bot = bot

    @discord.ui.button(custom_id="left_button", style=discord.ButtonStyle.primary, label="<") 
    async def button1_callback(self, button, interaction: discord.Interaction):
        if self.pos - self.level_range <= 0:
            await interaction.response.defer()
            return
        self.pos -= self.level_range
        info: list = self.get_info(self.pos, self.level_range)
        await interaction.response.edit_message(embed=await self.make_embed(*info, self.pos, self.level_range, self.bot))

    @discord.ui.button(custom_id="right_button", style=discord.ButtonStyle.primary, label=">") 
    async def button2_callback(self, button, interaction: discord.Interaction):
        self.pos += self.level_range
        info: list = self.get_info(self.pos, self.level_range)
        await interaction.response.edit_message(embed=await self.make_embed(*info, self.pos, self.level_range, self.bot))