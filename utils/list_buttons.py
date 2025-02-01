import discord

# level_range is how many levels is shown in the list
# have to pass in 2 functions into the class, get_info and make_embed
# get_info function gets the levels (or whatever) is needed when the left/right button is pressed
# make_embed makes the embed with the new info

class ListButtons(discord.ui.View):
    def __init__(self, level_range, get_info, make_embed, timeout = 180):
        super().__init__()

        self.pos = 1
        self.level_range = level_range
        self.get_info = get_info
        self.make_embed = make_embed

    @discord.ui.button(style=discord.ButtonStyle.primary, label="<") 
    async def button1_callback(self, button, interaction: discord.Interaction):
        if self.pos - self.level_range <= 0:
            await interaction.response.defer
            return
        self.pos -= self.level_range
        info: list = self.get_info(self.pos, self.level_range)
        await interaction.response.edit_message(embed=self.make_embed(*info, self.pos, self.level_range))

    @discord.ui.button(style=discord.ButtonStyle.primary, label=">") 
    async def button2_callback(self, button, interaction):
        self.pos += self.level_range
        info: list = self.get_info(self.pos, self.level_range)
        await interaction.response.edit_message(embed=self.make_embed(*info, self.pos, self.level_range))