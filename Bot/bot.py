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

# Command to check the status of a steam account
@client.command()
async def status(ctx, steam_id):
    await ctx.send(vacChecker.check_vac(KEY, steam_id))

# Command to add a steam account to the database
@client.command()
async def add(ctx, steam_id):
    await ctx.send("This command is not yet implemented!")

# Command to remove a steam account from the database
@client.command()
async def remove(ctx, steam_id):
    await ctx.send("This command is not yet implemented!")

# Help command
@client.command()
async def help(ctx):
    await ctx.send("status <steamID> - check the status of a specific account\n"
                   "check - check the VAC status of a your accounts\n"
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
