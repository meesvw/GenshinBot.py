import discord
from discord.ext import commands


# Create Magazine class
class Magazine(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def guide(self, ctx):
        embed = discord.Embed(
            color=discord.Colour.purple()
        )

        embed.add_field(
            name="Commands",
            value="`gi!help`"
        )

        embed.set_author(
            name=self.bot.user.name,
            icon_url=self.bot.user.avatar_url,
            url="https://github.com/meesvw/GenshinBot.py"
        )

        embed.set_footer(
            text=f"{self.bot.user.name} by mvw#2203",
        )

        await ctx.send(embed=embed)


# Setup cog
def setup(bot):
    bot.add_cog(Magazine(bot))
