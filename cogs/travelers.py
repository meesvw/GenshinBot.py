import ast
import discord
import os
import sqlite3
from datetime import datetime
from discord.ext import commands

# vars
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/genshin.db"


# Functions

# Print current time
def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


# Create user dict
def create_user(user_id):
    user_dict = {
        "level": "1",
        "currency": {"Mora": 0, "Primogems": 0},
        "Ingredients": {},
        "Materials": {},
        "Food": {}
    }

    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (:user_id, :user_dict, :status)",
                       {"user_id": user_id, "user_dict": f"{user_dict}", "status": "new"})
        connection.commit()
        connection.close()
        return "You're now a Traveler!"
    except sqlite3.IntegrityError:
        return "You're already a Traveler!"


# Get user dict from database
def get_user_dict(user_id):
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user_dict = cursor.fetchall()[0]
        connection.close()
        return user_dict
    except:
        return "error"


# Create Travelers class
class Travelers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    async def appear(self, ctx):

        # Create user in database
        output = create_user(ctx.author.id)
        await ctx.send(output)

    # Show Traveler profile
    @commands.command()
    async def profile(self, ctx):

        # Get user data from database
        user_list = get_user_dict(ctx.author.id)
        user_dict = ast.literal_eval(user_list[1])
        user_status = user_list[2]

        # Create user currency string
        currency_string = ""
        for currency in user_dict["currency"]:
            currency_string += f"{currency} - {user_dict['currency'][currency]}\n"

        # If user is new change embed
        if user_status == "new":
            embed = discord.Embed(
                description="Below you can see your inventory. "
                            "Here you can see your ingredients, materials, stats and currency. ",
                color=discord.Colour.purple()
            )
        else:
            embed = discord.Embed(
                color=discord.Colour.purple()
            )

        embed.add_field(
            name="Currency",
            value=f"{currency_string}"
        )

        embed.set_author(
            name=f"{ctx.author.name}'s Inventory",
            icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)


# Setup cog
def setup(bot):
    bot.add_cog(Travelers(bot))
