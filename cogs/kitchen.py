import ast
import asyncio
import discord
import os
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv


# Vars
load_dotenv()
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
COOKING_INGREDIENTS_LOCATION = f"{BOT_LOCATION[:-5]}data/Materials/Crafting Materials/Cooking Ingredients.txt"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/Database/genshin.db"


# Functions
async def get_user_database(user_id):
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user_list = cursor.fetchall()[0]
        connection.close()
        return user_list
    except:
        return "Error"


# Creates class
class Kitchen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Let users cook
    @commands.command()
    async def cook(self, ctx, food):

        embed = discord.Embed(
            color=discord.Colour.purple()
        )

        embed.set_footer(
            text=f"{self.bot.user.name} by mvw#2203",
            icon_url=self.bot.user.avatar_url
        )

        await ctx.send(embed=embed)

    # Shows recipe embed
    @commands.command()
    async def recipes(self, ctx):
        with open(COOKING_INGREDIENTS_LOCATION, "r") as file:
            ingredients_data = file.read()
            ingredients_dict = ast.literal_eval(ingredients_data)

        embed = discord.Embed(
            title="Recipes <:Adeptus_Temptation:803029881419333632>",
            description="Since there are so many recipes in Genshin Impact, "
                        "I have decided to port them over to a wiki on which "
                        "you can search for the specific foods.",
            color=discord.Colour.purple()
        )

        embed.add_field(
            name="Usage 🔧",
            value=f"To cook you simply use the following command:\n`{BOT_PREFIX}cook ItemName`",
            inline=False
        )

        embed.add_field(
            name="Wiki 📖",
            value="https://github.com/meesvw/GenshinBot.py/wiki/Cooking"
        )

        embed.set_footer(
            text=f"{self.bot.user.name} by mvw#2203",
            icon_url=self.bot.user.avatar_url
        )

        await ctx.send(embed=embed)


# Setup cog
def setup(bot):
    bot.add_cog(Kitchen(bot))
