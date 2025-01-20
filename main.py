from dotenv import load_dotenv
import os
import discord
from slash_commands.get_level import get_level_by_position, get_level_by_name 
from slash_commands.add_level import add_level

load_dotenv()
Token: str = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

guilds = [1330730208046743652]

@bot.slash_command(guilds=guilds, name="get_level_by_position", description="Gets a level by list position")
@discord.option("level_position", type=discord.SlashCommandOptionType.integer)
async def get_level_by_position_cmd(ctx: discord.ApplicationContext, level_position: int):
    embed = get_level_by_position(level_position)
    if embed == None:
        await ctx.respond(f"Invalid level position **( {level_position} )**")
        return
    await ctx.respond(embed=embed)

@bot.slash_command(guilds=guilds, name="get_level_by_name", description="Gets a level by level name")
@discord.option("level_name", type=discord.SlashCommandOptionType.string)
async def get_level_by_name_cmd(ctx: discord.ApplicationContext, level_name: str):
    embed = get_level_by_name(level_name)
    if embed == None:
        await ctx.respond(f"Invalid level name **( {level_name} )**")
        return
    await ctx.respond(embed=embed)

@bot.slash_command(guilds=guilds, name="add_level", description="Adds a new level")
async def add_level_cmd(ctx: discord.ApplicationContext):
    modal = add_level()
    await ctx.send_modal(modal=modal)

def main() -> None:
    print("Bot is running.")
    bot.run(token=Token)

if __name__ == "__main__":
    main()