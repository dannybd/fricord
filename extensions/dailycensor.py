""" Only allow 1 swear per 24 hours """
import asyncio
import discord
import re
from discord.ext import commands

from common import *

THIN_ICE_ROLES = {
    "dannybd-test": 812918168913182720,
    "gamescord": 812942511085322271,
    "rttftc": 812925753594871808,
}


class DailyCensor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def censor(self, message):
        if message.author == self.bot.user:
            return
        guild = message.guild
        guild_key = get_guild_key(guild)
        if guild_key not in THIN_ICE_ROLES:
            return
        if not re.match(".*fu+ck.*", message.content.lower()):
            return
        author = message.author
        channel = message.channel
        role = guild.get_role(THIN_ICE_ROLES[guild_key])
        if role in author.roles:
            await message.delete()
            await channel.send(
                "oopsie woopsie {} did a fuckie wuckie!".format(author.mention)
            )
            return
        await channel.send("That's your one cuss for the next 24 hours.")
        await author.add_roles(role)
        await asyncio.sleep(86400)
        await author.remove_roles(role)


def setup(bot):
    cog = DailyCensor(bot)
    bot.add_cog(cog)
