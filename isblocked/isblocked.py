import redbot.core
from redbot.core import Config, commands, checks
from redbot.core import commands
from redbot.core import checks
import discord
import asyncio
import re


class isblocked(commands.Cog):
    """Check to see if a user is blocking us"""
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    async def isblocking(self,ctx, message):
        """Is this user blocking us?"""
        if type(message) is int or type(message) is str:
            message = await ctx.fetch_message(int(message))
        else:
            await ctx.send("failed to get message.")
            await ctx.send(str(type(message)))
            return
        try:
            await message.add_reaction("\N{gear}")
        except discord.errors.Forbidden:
            await ctx.send(f"{message.author} has me blocked!")
            return
        await message.remove_reaction("\N{gear}",self.bot.user)
        await ctx.send(f"{message.author} is not blocking me.")
        


        
        


