from dotenv import load_dotenv
import os
import discord
from slash_commands.get_level import get_level_by_position, get_level_by_name, get_last_level
from slash_commands.list_levels import list_levels
from slash_commands.add_level import add_level
from slash_commands.delete_level import delete_level
from slash_commands.update_level_position import update_level_position

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

@bot.slash_command(guilds=guilds, name="list_levels", description="Lists all Coretop levels")
async def list_levels_cmd(ctx):
    embed, view = list_levels()
    await ctx.respond(embed=embed,view=view)

@bot.slash_command(guilds=guilds, name="add_level", description="Adds a new level")
async def add_level_cmd(ctx: discord.ApplicationContext):
    modal = add_level()
    await ctx.send_modal(modal=modal)

@bot.slash_command(guilds=guilds, name="delete_level", description="Deletes a new level")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
async def delete_level_cmd(ctx: discord.ApplicationContext, level_position: int):
    embed = delete_level(level_position)
    await ctx.respond(embed=embed)

@bot.slash_command(guilds=guilds, name="update_level_position", description="Changes the position of a level")
@discord.option("old_position", type=discord.SlashCommandOptionType.integer)
@discord.option("new_position", type=discord.SlashCommandOptionType.integer)
async def update_level_position_cmd(ctx: discord.ApplicationContext, old_position: int, new_position):
    embed = update_level_position(old_position, new_position)
    await ctx.respond(embed=embed)

def main():
    print("Bot is running.")
    bot.run(token=Token)

if __name__ == "__main__":
    main()