import ast
import discord
import os
import sqlite3
from datetime import datetime
from discord.ext import commands


# vars
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/Database/genshin.db"


# Functions

# Print current time
def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


# Get user dict from database
async def get_user_dict(user_id):
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        user_list = cursor.fetchall()
        if user_list:
            connection.close()
            return user_list[0]
        else:
            return "User unknown"
    except:
        return "Error"


# Insert user dict into database
async def insert_user_dict(user_id, user_dict):
    return


# Create Travelers class
class Chief(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create Traveler profile.
    @commands.command()
    @commands.is_owner()
    async def gib(self, ctx, user: discord.User, *, option):
        # Syntax usage: gi!gib mvw cooking ingredients|butter|1
        option_list = option.split("|")
        if len(option_list) != 3:
            return await ctx.send("Wrong syntax used.")

        # Vars
        category = option_list[0].title()
        item = option_list[1].title()
        try:
            amount = int(option_list[2])
        except ValueError:
            return await ctx.send(f"`{option_list[2]}` is not a number.")

        # Check if category is cooking ingredients
        if category == "Cooking Ingredients":
            with open(f"{BOT_LOCATION[:-5]}data/Items/Materials/Crafting Materials/Cooking Ingredients.txt", "r") as file:
                items_data = file.read()
                items_dict = ast.literal_eval(items_data)

            try:
                item_dict = items_dict[item]
                return await ctx.send(f"`{amount}x {item}` added to `{user.name}`.")
            except KeyError:
                return await ctx.send(f"`{item}` is not a item.")

        # Check if category is food
        if category == "Food":
            with open(f"{BOT_LOCATION[:-5]}items/Food.txt") as file:
                items_data = file.read()
                items_dict = ast.literal_eval(items_data)

        else:
            return await ctx.send(f"`{category}` is not a valid category.")


# Setup cog
def setup(bot):
    bot.add_cog(Chief(bot))
