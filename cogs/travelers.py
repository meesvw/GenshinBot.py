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


# Create user dict
async def create_user(user_id):
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        output = cursor.fetchall()

        # Check if player exists
        if output:
            connection.close()
            return "User exists"

        else:
            # Get basic user information
            with open(f"{BOT_LOCATION[:-5]}data/Database/Basic User.txt", "r") as file:
                user_data = file.read()
                user_dict = ast.literal_eval(user_data)

            # Get basic Traveler information
            with open(f"{BOT_LOCATION[:-5]}data/Characters/Traveler.txt", "r") as file:
                character_data = file.read()
                character_dict = ast.literal_eval(character_data)

            # Give user the Traveler as starting character
            user_dict["Characters"]["Traveler"] = {
                "Artifacts": character_dict["Artifacts"],
                "Weapon": character_dict["Weapon"],
                "EXP": 0,
                "Level": 1,
                "Ascension Level": 0
            }

            # Give user the basic Dull Sword in inventory
            user_dict["Inventory"]["Weapons"]["Dull Blade"] = {
                "EXP": 0,
                "Level": 1,
                "Ascension Level": 0
            }

            # Inserts the user data into the database
            cursor.execute("INSERT INTO users VALUES (:user_id, :user_dict, :status)",
                           {"user_id": user_id, "user_dict": f"{user_dict}", "status": "new"})
            connection.commit()
            connection.close()
            print(f"{current_time()} - User created with ID: {user_id}")
            return "User created"
    except:
        return "Error"


# Remove User from database
async def remove_user(user_id):
    try:
        connection = sqlite3.connect(USERS_DATABASE)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        output = cursor.fetchall()
        if output:
            cursor.execute(f"DELETE FROM users WHERE user_id = {user_id}")
            connection.commit()
            connection.close()
            print(f"{current_time()} - User removed with ID: {user_id}")
            return "User removed"
        else:
            connection.close()
            return "User unknown"
    except:
        return "Error"


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


# Create profile embed
async def create_profile_embed(ctx, self, user_list):
    # Vars
    user_dict = ast.literal_eval(user_list[1])
    user_active_character = user_dict["Character"]
    user_active_weapon = user_dict["Characters"][user_active_character]["Weapon"]

    with open(f"{BOT_LOCATION[:-5]}data/Characters/{user_active_character}.txt", "r") as file:
        character_data = file.read()
        character_dict = ast.literal_eval(character_data)

    # Embed
    embed = discord.Embed(
        color=discord.Colour.purple()
    )

    embed.set_author(
        name=f"{ctx.author.name}'s Profile",
        icon_url=ctx.author.avatar_url
    )

    embed.add_field(
        name="Adventure Rank <:Adventure_Experience:803389956768661556>",
        value=f"Level: `{user_dict['Adventure Rank']}`\n"
              f"EXP: `{user_dict['Adventure EXP']}/100`",
        inline=False
    )

    # Get Traveler level
    traveler_exp = user_dict["Characters"][user_active_character]["EXP"]
    traveler_level = user_dict["Characters"][user_active_character]["Level"]
    traveler_ascension_level = user_dict["Characters"][user_active_character]["Ascension Level"]

    embed.add_field(
        name="Traveler <:PaimonIcon:804459171906846761>",
        value=f"Name: `{user_active_character}`\nEXP: `{traveler_exp}/100`\nLevel: `{traveler_level}`\nAscension Level: `{traveler_ascension_level}`"
    )

    # Get weapon stats
    weapon_string = f"Name: `{user_active_weapon}`\n"
    weapon_user_dict = user_dict["Inventory"]["Weapons"][user_active_weapon]
    for item in weapon_user_dict:
        if item == "EXP":
            weapon_string += f"{item}: `{weapon_user_dict[item]}/100`\n"
        else:
            weapon_string += f"{item}: `{weapon_user_dict[item]}`\n"

    embed.add_field(
        name="Current Weapon :crossed_swords:",
        value=weapon_string
    )

    # Get Traveler artifacts
    artifacts_string = ""
    for artifact in user_dict["Characters"][user_active_character]["Artifacts"]:
        artifacts_string += f"`{user_dict['Characters'][user_active_character]['Artifacts'][artifact]}`\n"

    embed.add_field(
        name="Artifacts <:Icon_Artifacts:804459458755035179>",
        value=artifacts_string
    )

    embed.set_thumbnail(
        url=character_dict['Thumbnail Link']
    )

    embed.set_footer(
        text=f"{self.bot.user.name} by mvw#2203",
        icon_url=self.bot.user.avatar_url
    )

    return embed


# Create User unknown embed
async def create_user_unknown_embed(ctx, self):
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
async def create_error_embed(ctx, self):
    embed = discord.Embed(
        description=f"Something went wrong! Please try again.",
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


# Create Travelers class
class Travelers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Create User profile.
    @commands.command()
    async def appear(self, ctx):
        # Create user in database
        output = await create_user(ctx.author.id)
        await ctx.send(output)

    # Remove User profile
    @commands.command()
    async def disappear(self, ctx):
        # Remove user in database
        output = await remove_user(ctx.author.id)
        await ctx.send(output)

    # Show User profile
    @commands.command()
    async def profile(self, ctx):
        user_list = await get_user_list(ctx.author.id)
        if user_list == "User unknown":
            embed = await create_user_unknown_embed(ctx, self)
            return await ctx.send(embed=embed)
        if user_list == "Error":
            embed = await create_error_embed(ctx, self)
            return await ctx.send(embed=embed)
        else:
            embed = await create_profile_embed(ctx, self, user_list)
            await ctx.send(embed=embed)


# Setup cog
def setup(bot):
    bot.add_cog(Travelers(bot))
