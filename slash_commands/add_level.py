import discord

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Level Name, ID (EX: Requiem,12345)"))
        self.add_item(discord.ui.InputText(label="Level Position"))
        self.add_item(discord.ui.InputText(label="Level Creators"))
        self.add_item(discord.ui.InputText(label="Level Tier.? (possibly)"))
        self.add_item(discord.ui.InputText(label="Video Link"))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Level Added")
        embed.add_field(name="Short Input", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

def add_level():
    return MyModal(title="Add Level (please format correctly)")