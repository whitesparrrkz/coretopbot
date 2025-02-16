import discord
import asyncio

import discord.ext
from slash_commands.silly.video_manager import VideoManager
from utils.get_discord_file import get_tier_png

async def play_guesser(ctx: discord.ApplicationContext, bot: discord.Bot, video_manager: VideoManager, is_gif):
    level, file = await video_manager.get_level(is_gif)
    embed = discord.Embed(title="Guess the level!", color=discord.Colour.blue())
    embed.set_image(url="attachment://" + file.filename)
    await ctx.respond(embed=embed, files=[file])
    timeout = 5
    end_time = asyncio.get_event_loop().time() + timeout  

    def check(message: discord.Message):
        return message.channel == ctx.channel and not message.author.bot
    win = False
    while asyncio.get_event_loop().time() < end_time:
        try:
            time_left = max(0, end_time - asyncio.get_event_loop().time()) 
            message: discord.Message = await bot.wait_for("message", check=check, timeout=time_left)
            if message:
                if message.content.lower() == level["level_name"].lower():
                    win = True
                    break
        except asyncio.TimeoutError:
            pass
    if win:
        embed = discord.Embed(title="Correct!", color=discord.Colour.green())
        embed.add_field(name="", value=f"The level was: {level["level_name"]}")
    else:
        embed = discord.Embed(title="lol", color=discord.Colour.dark_red())
        embed.add_field(name="", value="you suck")
    await ctx.send(embed=embed)
