import discord
import asyncio

import discord.ext
from slash_commands.silly.video_manager import VideoManager

channels: set = set()

# is_interaction, False when command is called via slash command, True if calling the command 
async def play_guesser(ctx: discord.ApplicationContext, interaction: discord.Interaction, bot: discord.Bot, video_manager: VideoManager, options):
    if ctx is not None:
        channel_id = ctx.channel_id
        if channel_id in channels:
            embed = discord.Embed(title="There's already a guesser game happening in this channel, mr silly", color=discord.Colour.red())
            await ctx.respond(embed=embed, ephemeral=True)
            return
    else:
        channel_id = interaction.channel_id
        if channel_id in channels:
            embed = discord.Embed(title="There's already a guesser game happening in this channel, mr silly", color=discord.Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    channels.add(channel_id)
    try:
        if ctx is not None:
            await ctx.defer()
        else:
            await interaction.response.defer()
        level, file = await video_manager.get_level(options["include_junkyard"]["value"], options["is_gif"]["value"])
        embed = discord.Embed(title="Guess the level!", color=discord.Colour.blue())
        embed.set_image(url="attachment://" + file.filename)

        modstrnerf = ""
        modstrbuff = ""
        footerstr = "("
        first = True
        points = 10
        for k, v in options.items():
            if v["mult"] > 1:
                modstrbuff += f"🟢 {v["name"]} ({v["mult"]}x)\n"
            elif v["mult"] < 1:
                modstrnerf += f"🔴 {v["name"]} ({v["mult"]}x)\n"
            points *= v["mult"]

            if not first:
                footerstr += ", "
            footerstr += f"{k}={v["value"]}"
            first = False
        footerstr += ")"
        embed.add_field(name=f"Points: {points}", value=modstrbuff+modstrnerf)
        embed.set_footer(text=footerstr)
        # the bots message that sends the image/gif
        if ctx is not None:
            image_message = await ctx.respond(embed=embed, files=[file])
        else:
            image_message = await interaction.followup.send(embed=embed, files=[file])
        end_time = asyncio.get_event_loop().time() + options["time_limit"]["value"]

        def check(message: discord.Message):
            return message.channel.id == channel_id and not message.author.bot
        win = False
        player_message: discord.Message = None
        while asyncio.get_event_loop().time() < end_time:
            try:
                time_left = max(0, end_time - asyncio.get_event_loop().time()) 
                message: discord.Message = await bot.wait_for("message", check=check, timeout=time_left)
                if message:
                    if message.content.lower() == level["level_name"].lower():
                        win = True
                        player_message = message
                        break
            except asyncio.TimeoutError:
                pass
        if win:
            embed = discord.Embed(title="Correct!", color=discord.Colour.green())
            embed.add_field(name="", value=f"The level was: {level["level_name"]}")
            await player_message.reply(embed=embed, view=PlaybackButton(bot, video_manager, options))
        else:
            embed = discord.Embed(title="lol", color=discord.Colour.light_gray())
            embed.add_field(name="", value="you suck")
            await image_message.reply(embed=embed, view=PlaybackButton(bot, video_manager, options))
    finally:
        channels.remove(channel_id)

def make_options(include_junkyard, is_gif, time_limit):
    options: dict = {}
    # Name : (mult)
    # mult < 1, nerf
    # mult = 1, normal
    # mult > 1, buff
    if include_junkyard:
        options["include_junkyard"] = {"name": "Entire List", "value": include_junkyard, "mult": 1}
    else:
        options["include_junkyard"] = {"name": "Main List", "value": include_junkyard, "mult": 0.5}
    if is_gif:
        options["is_gif"] = {"name": "GIF", "value": is_gif, "mult": 1}
    else:
        options["is_gif"] = {"name": "Static Image","value": is_gif, "mult": 1.5}
    if time_limit <= 5:
        options["time_limit"] = {"name": "Fast Guess", "value": time_limit, "mult": 1.5}
    elif time_limit >= 16:
        options["time_limit"] = {"name": "Slow Guess","value": time_limit, "mult": 0.5}
    else:
        options["time_limit"] = {"name": "Normal Speed Guess","value": time_limit, "mult": 1}
    return options

class PlaybackButton(discord.ui.View):
    def __init__(self, bot: discord.Bot, video_manager, options):
        super().__init__()
        self.bot = bot
        self.video_manager = video_manager
        self.options = options
    
    @discord.ui.button(style=discord.ButtonStyle.secondary, label="Play Again")
    async def callback(self, button, interaction: discord.Interaction):
        await play_guesser(None, interaction, self.bot, self.video_manager, self.options)