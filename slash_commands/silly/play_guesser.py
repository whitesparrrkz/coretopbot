import discord
import asyncio

import discord.ext

async def play_guesser(ctx: discord.ApplicationContext, bot: discord.Bot):
    await ctx.defer()
    timeout = 3
    end_time = asyncio.get_event_loop().time() + timeout  

    def check(message):
        return message.channel == ctx.channel and not message.author.bot

    while asyncio.get_event_loop().time() < end_time:
        try:
            message = await bot.wait_for("message", check=check, timeout=0.5)
            time_left = max(0, end_time - asyncio.get_event_loop().time()) 
            await ctx.send(content=f"Message: {message.content}\n{time_left:.2f} seconds left")
        except asyncio.TimeoutError:
            pass
    await ctx.send("Lol")
