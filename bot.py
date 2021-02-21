#! /usr/bin/python3

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


bot = commands.Bot(
    command_prefix="carlson ",
    description=(
        "Carl Carlson the Second, Son of Carl: "
        + "a Discord bot for the Hawai'i Fridays"
    ),
    intents=intents,
)


@bot.event
async def on_ready():
    logging.info("Connected as {0.user} and ready!".format(bot))


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
