import discord

# level_range is how many levels is shown in the list
# have to pass in 2 functions into the class, get_info and make_embed
# get_info function gets the levels (or whatever) is needed when the left/right button is pressed
# make_embed makes the embed with the new info

class ListButtons(discord.ui.View):
    def __init__(self, level_range, get_info, make_embed, bot: discord.Bot = None, timeout = None):
        super().__init__(timeout=timeout)

        self.pos = 1
        self.level_range = level_range
        self.get_info = get_info
        self.make_embed = make_embed
        self.bot = bot

    @discord.ui.button(custom_id="left_button", style=discord.ButtonStyle.primary, label="<") 
    async def button1_callback(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.pos - self.level_range <= 0:
            return
        self.pos -= self.level_range
        info: list = self.get_info(self.pos, self.level_range)
        await interaction.followup.edit_message(interaction.message.id, embed=self.make_embed(*info, self.pos, self.level_range, self.bot))

    @discord.ui.button(custom_id="right_button", style=discord.ButtonStyle.primary, label=">") 
    async def button2_callback(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        self.pos += self.level_range
        info: list = self.get_info(self.pos, self.level_range)
        await interaction.followup.edit_message(interaction.message.id, embed=self.make_embed(*info, self.pos, self.level_range, self.bot))