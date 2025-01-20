from dotenv import load_dotenv
import os
import discord

load_dotenv()
Token: str = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

@bot.slash_command(name="get_level", description="Gets a level by list position")
@discord.option("pos", type=discord.SlashCommandOptionType.integer)
async def getLevel(ctx: discord.ApplicationContext, pos: int):
    await ctx.respond(f"Not yet... u gave {pos}")

def main() -> None:
    print("Bot is running.")
    bot.run(token=Token)

if __name__ == "__main__":
    main()