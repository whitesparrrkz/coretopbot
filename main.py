import discord.ext.commands
from dotenv import load_dotenv
import os
import discord
import discord.ext

from slash_commands.level.get_level import get_level_by_position, get_level_by_name, get_last_level
from slash_commands.level.list_levels import list_levels
from slash_commands.level.add_level import add_level
from slash_commands.level.delete_level import delete_level
from slash_commands.level.update_level_position import update_level_position

from slash_commands.victor.add_victor import add_victor
from slash_commands.victor.pop_victor import pop_victor
from slash_commands.victor.get_victor import get_victor

from slash_commands.junkyard.add_junkyard_level import add_junkyard_level
from slash_commands.junkyard.list_junkyard_levels import list_junkyard_levels
from slash_commands.junkyard.delete_junkyard_level import delete_junkyard_level

load_dotenv()
Token: str = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

commands = discord.ext.commands

guilds = [1330730208046743652]

announcements_id = 1332912849705631795

level = discord.SlashCommandGroup("level", "everything that deals with normal levels")
victor = discord.SlashCommandGroup("victor", "everything that deals with victors")
junkyard = discord.SlashCommandGroup("junkyard", "everything that deals with junkyard levels")

@level.command(name="get_level_by_position", description="Gets a level by list position")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
async def get_level_by_position_cmd(ctx: discord.ApplicationContext, level_position: int):
    embed = get_level_by_position(level_position)
    await ctx.respond(embed=embed)

@level.command(name="get_level_by_name", description="Gets a level by level name")
@discord.option("level_name", type=discord.SlashCommandOptionType.string)
async def get_level_by_name_cmd(ctx: discord.ApplicationContext, level_name: str):
    embed = get_level_by_name(level_name)
    await ctx.respond(embed=embed)

@level.command(name="get_last_level", description="Gets the last level in the list (so easy...)")
async def get_level_by_name_cmd(ctx: discord.ApplicationContext):
    embed = get_last_level()
    await ctx.respond(embed=embed)

@level.command(name="list_levels", description="Lists all Coretop levels")
async def list_levels_cmd(ctx):
    embed, view = list_levels()
    await ctx.respond(embed=embed,view=view)

@level.command(name="add_level", description="Adds a new level")
@discord.option("send_announcement", type=discord.SlashCommandOptionType.boolean)
@commands.has_role("coretop admin")
async def add_level_cmd(ctx: discord.ApplicationContext, send_announcement):
    modal = add_level(bot, announcements_id, send_announcement)
    await ctx.send_modal(modal=modal)

@level.command(name="delete_level", description="Deletes a level")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
@commands.has_role("coretop admin")
async def delete_level_cmd(ctx: discord.ApplicationContext, level_position: int):
    embed = delete_level(level_position)
    await ctx.respond(embed=embed)

@level.command(name="update_level_position", description="Changes the position of a level")
@discord.option("old_position", type=discord.SlashCommandOptionType.integer)
@discord.option("new_position", type=discord.SlashCommandOptionType.integer)
@commands.has_role("coretop admin")
async def update_level_position_cmd(ctx: discord.ApplicationContext, old_position, new_position):
    embed = update_level_position(old_position, new_position)
    await ctx.respond(embed=embed)

@victor.command(name="add_victor_by_level_position", description="Adds a victor to a level by level position")
@discord.option("victor_name", type=discord.SlashCommandOptionType.string)
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
@commands.has_role("coretop admin")
async def add_victor_by_level_position_cmd(ctx: discord.ApplicationContext, victor_name: str, level_position):
    embed = add_victor(victor_name, level_position)
    await ctx.respond(embed=embed)

@victor.command(name="pop_victor_by_level_position", description="Removes the last victor from a level by level position")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
@commands.has_role("coretop admin")
async def pop_victor_by_level_position_cmd(ctx: discord.ApplicationContext, level_position):
    embed = pop_victor(level_position)
    await ctx.respond(embed=embed)

@victor.command(name="get_victor", description="Displays information about a victor")
@discord.option("victor_name", type=discord.SlashCommandOptionType.string)
async def get_victor_cmd(ctx: discord.ApplicationContext, victor_name: str):
    embed, file = get_victor(victor_name)
    await ctx.respond(embed=embed, files=[file])

@junkyard.command(name="add_junkyard_level", description="Adds a new junkyard level (Easy/Medium demons)")
@discord.option("level_name", type=discord.SlashCommandOptionType.string)
@discord.option("level_tier", type=discord.SlashCommandOptionType.string)
@discord.option("level_url", type=discord.SlashCommandOptionType.string)
async def add_junkyard_level_cmd(ctx: discord.ApplicationContext, level_name, level_tier, video_url):
    embed = add_junkyard_level(level_name, level_tier, video_url)
    await ctx.respond(embed=embed)

@junkyard.command(name="list_junkyard_levels", description="Lists all junkyard levels (ordered by additon date, not difficulty)")
async def list_junkyard_levels_cmd(ctx: discord.ApplicationContext):
    embed, view = list_junkyard_levels()
    await ctx.respond(embed=embed,view=view)

@junkyard.command(name="delete_junkyard_level", description="Deletes a junkyard level by a given name")
@discord.option("level_name", type=discord.SlashCommandOptionType.string)
async def delete_junkyard_level_cmd(ctx: discord.ApplicationContext, level_name):
    embed = delete_junkyard_level(level_name)
    await ctx.respond(embed=embed)

bot.add_application_command(level)
bot.add_application_command(victor)
bot.add_application_command(junkyard)

def main():
    print("Bot is running.")
    bot.run(token=Token)

if __name__ == "__main__":
    main()