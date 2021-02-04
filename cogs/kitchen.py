import ast
import asyncio
import discord
import os
import random
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv


# Vars
load_dotenv()
BOT_PREFIX = os.getenv("BOT_PREFIX")
BOT_LOCATION = f"{os.path.dirname(os.path.abspath(__file__))}/"
COOKING_INGREDIENTS_LOCATION = f"{BOT_LOCATION[:-5]}data/Items/Materials/Crafting Materials/Cooking Ingredients.txt"
FOOD_LOCATION = f"{BOT_LOCATION[:-5]}data/Items/Food.txt"
USERS_DATABASE = f"{BOT_LOCATION[:-5]}data/Database/genshin.db"


# Functions

# Get user dict from database
async def get_user_list(user_id):
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


# Check if User has the needed ingredients
async def check_user_ingredients(user_dict, needed_ingredients_dict):
    user_ingredients_dict = user_dict["Inventory"]["Materials"]["Crafting Materials"]["Cooking Ingredients"]
    try:
        for item in needed_ingredients_dict:
            result = needed_ingredients_dict[item]-user_ingredients_dict[item]
            if result < 0:
                return "Missing Amount Cooking Ingredients"
    except KeyError:
        return "Missing Cooking Ingredients"


# Create User unknown embed
async def create_user_unknown_embed(self, ctx):
    embed = discord.Embed(
        description=f"It looks like you don't have a profile yet.\n"
                    f"Use: `{BOT_PREFIX}appear` to create a profile.",
        color=discord.Colour.purple()
    )

    embed.set_author(
        name=f"Hey {ctx.author.name}",
        icon_url=ctx.author.avatar_url
    )

    embed.set_footer(
        text=f"{self.bot.user.name} by mvw#2203",
        icon_url=self.bot.user.avatar_url
    )

    return embed


# Create Error embed
async def create_error_embed(self, ctx):
    embed = discord.Embed(
        description=f"Something went wrong! Please try again.",
        color=discord.Colour.purple()
    )

    embed.set_author(
        name=f"Hey {ctx.author.name}",
        icon_url=ctx.author.avatar_url
    )

    embed.set_footer(
        text=f"{self.bot.user.name}",
        icon_url=self.bot.user.avatar_url
    )

    return embed


# Create unknown food embed
async def create_unknown_food_embed(self, ctx, food):
    embed = discord.Embed(
        title=f"Unknown Food: `{food}`",
        description="Maybe you misspelled something?",
        color=discord.Colour.purple()
    )

    embed.add_field(
        name="Wiki",
        value="See all recipes on the wiki:\n"
              "https://github.com/meesvw/GenshinBot.py/wiki/Cooking"
    )

    embed.set_footer(
        text=self.bot.user.name,
        icon_url=self.bot.user.avatar_url
    )

    return embed


# Creates class
class Kitchen(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Let users cook
    @commands.command()
    async def cook(self, ctx, *, food):
        # Check if user exists or error occurred
        user_dict = await get_user_list(ctx.author.id)
        if user_dict == "User unknown":
            embed = await create_user_unknown_embed(self, ctx)
            return await ctx.send(embed=embed)
        if user_dict == "Error":
            embed = await create_error_embed(self, ctx)
            return await ctx.send(embed=embed)

        # Set User Dict
        user_dict = ast.literal_eval(user_dict[1])

        # Edit food string
        food = food.title()

        # Make cooking ingredients dict
        with open(f"{COOKING_INGREDIENTS_LOCATION}", "r") as file:
            cooking_ingredients_data = file.read()
            cooking_ingredients_dict = ast.literal_eval(cooking_ingredients_data)

        # Make food dict
        with open(f"{FOOD_LOCATION}", "r") as file:
            food_data = file.read()
            food_dict = ast.literal_eval(food_data)

        # See if food exists
        fail = 0
        try:
            needed_ingredients_dict = cooking_ingredients_dict[food]["Recipe"]
        except KeyError:
            fail += 1

        try:
            needed_ingredients_dict = food_dict[food]["Recipe"]
        except KeyError:
            fail += 1

        if fail == 2:
            embed = await create_unknown_food_embed(self, ctx, food)
            return await ctx.send(embed=embed)

        await check_user_ingredients(user_dict, cooking_ingredients_dict)

    # Shows recipe embed
    @commands.command()
    async def recipes(self, ctx):
        embed = discord.Embed(
            title="Recipes <:Adeptus_Temptation:803029881419333632>",
            description="Genshin Impact has many recipes to learn and discover. "
                        "To make cooking easy all recipes are listen on the wiki.",
            color=discord.Colour.purple()
        )

        embed.add_field(
            name="Usage 🔧",
            value=f"To cook simply use: `{BOT_PREFIX}cook foodName`",
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
