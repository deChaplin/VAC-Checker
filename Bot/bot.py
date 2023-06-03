import asyncio

import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
from dotenv import load_dotenv
import random
from Checker import vacChecker

# Setting up the client and intents
intents = discord.Intents.all()
# Setting up the bots prefix
client = commands.Bot(command_prefix='!', intents=intents)
# Setting up the status to cycle through
status = cycle(["your steam accounts!", "to see who gets banned!"])

load_dotenv()
TOKEN = os.getenv('TOKEN')
KEY = os.getenv('KEY')

@client.event
async def on_ready():
    vacChecker.start_up()
    print('Bot is ready!')
    change_status.start()

# Remove the default help command
client.remove_command('help')

# Command to check the VAC status of a steam account
@client.command()
async def check(ctx, steam_name):
    steam_id = vacChecker.get_steamid(steam_name)
    if steam_id:
        vac_status = vacChecker.get_vac_status(steam_id)
        game_status = vacChecker.get_game_status(steam_id)
        if vac_status == "None":
            await ctx.send(f"{steam_name} has no VAC bans!")
        else:
            await ctx.send(f"{steam_name} has {vac_status} VAC bans!")
    else:
        await ctx.send(f"{steam_name} is not in the database!")

@client.command()
async def status(ctx, steam_name):
    #account = vacChecker.get_steamid(steam_name)

    #await ctx.send("Account - " + vacChecker.check_vac())
    await ctx.send("all good - " + steam_name)

# Command to add a steam account to the database
@client.command()
async def add(ctx, steam_id):
    if steam_id:
        vacChecker.add_account(steam_id, "Test", "None", "None")
        await ctx.send(f"{steam_id} has been added to the database!")
    else:
        await ctx.send(f"{steam_id} is not a valid steam account!")

# Command to remove a steam account from the database
@client.command()
async def remove(ctx, steam_id):
    if steam_id:
        vacChecker.remove_account(steam_id)
        await ctx.send(f"{steam_id} has been removed from the database!")
    else:
        await ctx.send(f"{steam_id} is not a valid steam account!")

# Help command
@client.command()
async def help(ctx):
    await ctx.send("status <steamID> - check the status of a specific account\n"
                   "check <steamID> - check the VAC status of a specific account\n"
                   "add <steamID> - add a steam account to the database\n"
                   "remove <steamID> - remove a steam account from the database\n"
                   )

# Looping through the status
status = cycle(["your steam accounts!", " who gets banned!", " you", " people get banned"])
@tasks.loop(seconds=1)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(status))))
    await asyncio.sleep(3)

client.run(TOKEN)
