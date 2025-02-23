import discord
import requests

async def get_guesser_player(ctx: discord.ApplicationContext, user: discord.Member):
    await ctx.defer()
    url = f"http://localhost:8080/coretop/api/guesserPlayer/getGuesserPlayerByUserId?user_id={user.id}"
    embed = discord.Embed(title=f"{user.name}", color=discord.Colour.blue())
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.exceptions.RequestException()
        player = response.json()
    except:
        player = {"points": 0, "highest_streak": 0, "best_guess": 0}
        embed.set_footer(text="Never Played")
    embed.add_field(name="Total Points", value=player["points"], inline=True)
    embed.add_field(name="Highest Streak", value=player["highest_streak"], inline=True)
    embed.add_field(name="Best Guess", value=player["best_guess"], inline=True)
    avatar = user.guild_avatar
    if avatar == None:
        avatar = user.avatar
    embed.set_thumbnail(url=avatar.url)
    await ctx.respond(embed=embed)