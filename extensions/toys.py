""" Contains some fun commands that aren't that useful """
import datetime
import discord
import json
import re
from discord.ext import commands


def plural(num, noun):
    return "{} {}{}".format(num, noun, "" if num == 1 else "s")


class Toys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def fun_replies(self, message):
        if message.author == self.bot.user:
            return
        content = message.content.lower()
        channel = message.channel
        if re.match("good ?night( to)? honu.*", content):
            await message.add_reaction("🛌")
            await message.add_reaction("🐢")
            await message.add_reaction("💤")
            return
        if re.match("good ?morning.+honu.*", content):
            await message.add_reaction("🌅")
            await message.add_reaction("🐢")
            return
        if re.match("whose dork\\??", content):
            await channel.send("our dork!")
            return
        if content == "+normal":
            with open("logs/normal.json", "r") as f:
                data = json.load(f)
            if data == None:
                data = {}
            last_normal = data.get("last_normal")
            now = datetime.datetime.now()
            data["last_normal"] = now.timestamp()
            with open("logs/normal.json", "w") as f:
                json.dump(data, f)
            if last_normal == None:
                await channel.send("Starting the clock.")
                return
            then = datetime.datetime.fromtimestamp(last_normal)
            delta = now - then
            days = delta.days
            seconds = delta.seconds
            hours = seconds // 3600
            seconds -= hours * 3600
            minutes = seconds // 60
            seconds -= minutes * 60
            await channel.send(
                (
                    "Reset the clock!\nIt has been {}, {}, {}, and {} "
                    + "since the Fridays had a normal one."
                ).format(
                    plural(days, "day"),
                    plural(hours, "hour"),
                    plural(minutes, "minute"),
                    plural(seconds, "second"),
                ),
                file=discord.File("extensions/normalone.png"),
            )

    @commands.command(hidden=True, aliases=["hurray"])
    async def hooray(self, ctx):
        await ctx.send("🥳🎉🎊✨")


def setup(bot):
    cog = Toys(bot)
    bot.add_cog(cog)
