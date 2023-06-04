import asyncio
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
from dotenv import load_dotenv
import random
from Checker import vacChecker
import guild_database

# Setting up the client and intents
intents = discord.Intents.all()
# Setting up the bots prefix
DEFAULT_PREFIX = '!'

async def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)
    else:
        if guild_database.check_guild(message.guild.id):
            prefix = guild_database.get_prefix(message.guild.id)
            return commands.when_mentioned_or(prefix)(client, message)
        else:
            guild_database.add_guild(message.guild.id, DEFAULT_PREFIX)
            return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)

client = commands.Bot(command_prefix=get_prefix, intents=intents)
# Setting up the status to cycle through
status = cycle(["your steam accounts!", "to see who gets banned!"])

load_dotenv()
TOKEN = os.getenv('TOKEN')
KEY = os.getenv('KEY')
# Remove the default help command
client.remove_command('help')

# ======================================================================================================================
# Standard Events
# ======================================================================================================================


@client.event
async def on_ready():
    vacChecker.start_up()
    print('Bot is ready!')
    change_status.start()

    guild_database.create_database()


# On guild join
@client.event
async def on_guild_join(guild):
    guild_database.add_guild(guild.id, '!')
    print(f"Joined {guild.name}")


# On guild remove
@client.event
async def on_guild_remove(guild):
    guild_database.remove_guild(guild.id)
    print(f"Removed {guild.name}")


# On message
@client.event
async def on_message(message):
    mention = f'<@{client.user.id}>'
    if message.content == mention:
        await message.channel.send("My prefix is " + guild_database.get_prefix(message.guild.id))

    if message.content.startswith(guild_database.get_prefix(message.guild.id)):
        await client.process_commands(message)


# ======================================================================================================================
# Standard Commands
# ======================================================================================================================


# Command to change the bots prefix
@client.command()
async def setPrefix(ctx, prefix):
    client.command_prefix = prefix
    guild_database.update_prefix(ctx.guild.id, prefix)
    await ctx.send(f"Prefix changed to {prefix}")


# Command to check the current prefix
@client.command()
async def checkPrefix(ctx):
    prefix = guild_database.get_prefix(ctx.guild.id)
    await ctx.send(f"Current prefix is {prefix}")


# ======================================================================================================================
# VAC Checker Commands
# ======================================================================================================================


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
status = cycle(["your steam accounts!", " who gets banned!", " you 👀", " people get banned", str(guild_database.get_num_guilds()) + " servers!"])
status2 = ["your steam accounts!", " who gets banned!", " you 👀", " people get banned", str(guild_database.get_num_guilds()) + " servers!"]

@tasks.loop(seconds=1)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(random.choice(status2))))
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(status))))
    await asyncio.sleep(3)


client.run(TOKEN)
