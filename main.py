from dotenv import load_dotenv
import os
import discord
from slash_commands.get_level import get_level_by_position, get_level_by_name, get_last_level
from slash_commands.add_level import add_level
from slash_commands.delete_level import delete_level

load_dotenv()
Token: str = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

guilds = [1330730208046743652]

@bot.slash_command(guilds=guilds, name="get_level_by_position", description="Gets a level by list position")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
async def get_level_by_position_cmd(ctx: discord.ApplicationContext, level_position: int):
    embed = get_level_by_position(level_position)
    await ctx.respond(embed=embed)

@bot.slash_command(guilds=guilds, name="get_level_by_name", description="Gets a level by level name")
@discord.option("level_name", type=discord.SlashCommandOptionType.string)
async def get_level_by_name_cmd(ctx: discord.ApplicationContext, level_name: str):
    embed = get_level_by_name(level_name)
    await ctx.respond(embed=embed)

@bot.slash_command(guilds=guilds, name="get_last_level", description="Gets the last level in the list (so easy...)")
async def get_level_by_name_cmd(ctx: discord.ApplicationContext):
    embed = get_last_level()
    await ctx.respond(embed=embed)

@bot.slash_command(guilds=guilds, name="add_level", description="Adds a new level")
async def add_level_cmd(ctx: discord.ApplicationContext):
    modal = add_level()
    await ctx.send_modal(modal=modal)

@bot.slash_command(guilds=guilds, name="delete_level", description="Deletes a new level")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
async def delete_level_cmd(ctx: discord.ApplicationContext, level_position: int):
    embed = delete_level(level_position)
    await ctx.respond(embed=embed)

class MyView(discord.ui.View):
    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="⬅") 
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("mrrrrp")

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="➡️") 
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("meow")

@bot.slash_command(guilds=guilds, name="test", description="its a test u silly")
async def button(ctx):
    await ctx.respond(view=MyView())

def main():
    print("Bot is running.")
    bot.run(token=Token)

if __name__ == "__main__":
    main()