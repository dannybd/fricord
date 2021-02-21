import configparser
from discord.ext import commands


GUILDS = {
    "dannybd-test": 432741711786278913,
    "fricord": 772197524207173634,
    "gamescord": 749693607513948181,
    "rttftc": 811868570081296394,
}
INV_GUILDS = {v: k for k, v in GUILDS.items()}


def get_guild_key(guild):
    if guild.id not in INV_GUILDS:
        return None
    return INV_GUILDS[guild.id]


def is_in_guilds(*guild_keys):
    async def predicate(ctx):
        return get_guild_key(ctx.guild) in guild_keys
    return commands.check(predicate)


config = configparser.ConfigParser()
config.read("config.ini")
