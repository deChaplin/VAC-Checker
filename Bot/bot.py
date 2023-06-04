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
    check_vac.start()

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
    if message.author == client.user:
        return

    if not guild_database.check_guild(message.guild.id):
        guild_database.add_guild(message.guild.id, DEFAULT_PREFIX)

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
    await ctx.send(vacChecker.check_vac(KEY, steam_id, ctx.message.author.id))


# Command to add a steam account to the database
@client.command()
async def add(ctx, steam_id):
    name = vacChecker.add_account(KEY, steam_id, ctx.message.author.id)
    await ctx.send(f"{name} added to database!")


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


def get_guilds():
    try:
        guilds = guild_database.get_num_guilds()
        if guilds >= 1:
            return guilds
        else:
            return "0"
    except:
        print ("Error getting guilds")
        return "0"


@tasks.loop(seconds=1)
async def change_status():
    status2 = ["your steam accounts!", " who gets banned!", " you 👀", " people get banned",
               str(get_guilds()) + " servers!"]

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(random.choice(status2))))
    await asyncio.sleep(3)


# Loop to check for vac bans on all accounts every hour
@tasks.loop(minutes=60)
async def check_vac():

    # Get list of user ids from database
    # iterate through list to check all accounts belonging to user
    # send private message to user

    # Will run for the number of unique discord ids in the database

    discord_ids = vacChecker.get_discord_id()

    if discord_ids:
        for row in discord_ids:
            user = client.get_user(int(row[0]))
            if user is not None:
                msg = vacChecker.check_all(KEY, str(row[0]))
                if msg is not None:
                    await user.send(msg)
            else:
                print(f"User with ID {str(row[0])} not found.")

client.run(TOKEN)
