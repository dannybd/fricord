#! /usr/bin/python3

import asyncio
import datetime
import discord
import json
import logging
import os
import pymysql
import random
import re
import sys
import typing
import traceback
import glob

from common import *
from discord.ext import commands
from discord.ext.commands import guild_only

# Define logging levels
loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(
    format="%(asctime)s [%(process)d][%(name)s - %(levelname)s] - %(message)s",
    level=loglevel,
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler(),
    ],
)
if loglevel == "INFO":
    logging.getLogger("discord").setLevel(logging.WARNING)


intents = discord.Intents.default()
intents.members = True
intents.presences = True

default_help = commands.DefaultHelpCommand(
    no_category="Other Commands",
)


bot = commands.Bot(
    command_prefix=["carlson ", "Carlson "],
    description=(
        "Carl Carlson the Second, Son of Carl: "
        + "a Discord bot for the Hawai'i Fridays"
    ),
    help_command=default_help,
    intents=intents,
)


@bot.event
async def on_ready():
    logging.info("Connected as {0.user} and ready!".format(bot))


@bot.command(name="punish", hidden=True)
async def punish(ctx, *, member: typing.Optional[discord.Member]):
    if ctx.author.id not in [276520565458862081, 448896411036024832]:
        return
    if not member:
        await ctx.send("Couldn't find a user with that name")
        return
    await ctx.send("{}, you have crossed garlic for the last time".format(member.mention))
    await asyncio.sleep(1)
    await ctx.send("now")
    await asyncio.sleep(1)
    await ctx.send("_pewish_")
    nick, *rest = member.display_name.split("(")
    nick = re.sub(r'[lr]', 'w', nick)
    nick = re.sub(r'[LR]', 'W', nick)
    nick = re.sub(r'n([aeiou])', r'ny\1', nick)
    nick = re.sub(r'N([aeiou])', r'Ny\1', nick)
    nick = re.sub(r'N([AEIOU])', r'NY\1', nick)
    nick = re.sub(r'ove', 'uv', nick)
    nick = re.sub(r'OVE', 'UV', nick)
    nick = nick + "(" + " ".join(rest)
    await member.edit(nick=nick)


logging.info("Loading extensions...")
for extension in glob.glob("extensions/*.py"):
    try:
        ext = extension[:-3]
        ext = ext.replace("/", ".")
        logging.info("Loading {}".format(ext))
        bot.load_extension(ext)
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, traceback.format_exc())
        logging.warning("Failed to load extension {}\n{}".format(extension, exc))

logging.info("Starting!")
bot.run(config["discord"]["botsecret"])
logging.info("Done, closing out")
