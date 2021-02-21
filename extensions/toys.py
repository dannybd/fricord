""" Contains some fun commands that aren't that useful """
import discord
from discord.ext import commands


class Toys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def fun_replies(self, message):
        if message.author == self.bot.user:
            return
        content = message.content.lower()
        channel = message.channel
        if "goodnight honu" in content:
            await message.add_reaction("🛌")
            await message.add_reaction("🐢")

    @commands.command(hidden=True, aliases=["hurray"])
    async def hooray(self, ctx):
        await ctx.send("🥳🎉🎊✨")


def setup(bot):
    cog = Toys(bot)
    bot.add_cog(cog)
