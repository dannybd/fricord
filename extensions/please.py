""" Only allow 1 swear per 24 hours """
import asyncio
import discord
import re
import typing
from discord.ext import commands

from common import *

BAN_ROLES = {
    "fricord": 779091248311959634,
    "dannybd-test": 812918168913182720,
}

UNBANNABLE_ROLES = {
    "fricord": 784614064667230209,
    "dannybd-test": 812918168913182720,
}


class Please(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    async def please(self, ctx):
        """Ask carlson nicely to do something"""
        if ctx.invoked_subcommand:
            return
        await ctx.send("What can I do for you?")

    @is_in_guilds("dannybd-test")
    @please.command(name="ban", hidden=True)
    async def ban(
        self,
        ctx,
        member: typing.Optional[discord.Member],
        *,
        duration: typing.Optional[str],
    ):
        """Jokingly ban a user from Fricord"""
        guild = ctx.guild
        guild_key = get_guild_key(guild)
        if guild_key not in BAN_ROLES:
            await ctx.send("This isn't supported here.")
            return
        if not member:
            await ctx.send(
                "Gotta tell me who you want to ban. " + "Try @ mentioning them."
            )
            return
        if not duration:
            duration = "24h"
        if not re.match("^\\d+(h|hrs?|hours?)?$", duration.lower()):
            await ctx.send("Please use a duration measured in hours, like '24h'")
            return
        duration = int(re.search("\\d+", "24h")[0])

        author = ctx.author
        ban_role = guild.get_role(BAN_ROLES[guild_key])
        unbannable_role = (
            guild.get_role(UNBANNABLE_ROLES[guild_key])
            if guild_key in UNBANNABLE_ROLES
            else None
        )
        if unbannable_role in author.roles:
            await ctx.send("{} cannot be banned.".format(author.display_name))
            return
        if ban_role in author.roles:
            await ctx.send(
                "{} is already banned, and they probably deserved it.".format(
                    author.display_name
                )
            )
            return
        await author.add_roles(ban_role)
        await ctx.send(
            "{} has been banned for {} hours".format(author.display_name, duration)
        )
        if duration > 24 * 30:
            return
        await asyncio.sleep(3600 * duration)
        await author.remove_roles(ban_role)

    @is_in_guilds("gamescord")
    @please.command(name="punish", hidden=True)
    async def punish(self, ctx):
        if ctx.author.id not in [276520565458862081, 448896411036024832]:
            return
        await ctx.send("(psst, don't say please for this)")

    @is_in_guilds("gamescord")
    @please.command(name="jailbreak", hidden=True)
    async def jailbreak(self, ctx):
        """Jailbreak everyone from baby jail"""
        role = ctx.guild.get_role(749797161163816980)
        await ctx.message.delete()
        await ctx.send("**throws glass on floor** SCATTER!!")
        for member in role.members:
            await member.remove_roles(role)


def setup(bot):
    cog = Please(bot)
    bot.add_cog(cog)
