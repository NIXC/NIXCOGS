import redbot.core
from redbot.core import Config, commands, checks
import discord
import asyncio
import re


class isblocked(commands.Cog):
    """Check to see if a user is blocking us"""
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    @checks.is_owner()
    async def isblocking(self, ctx, message: discord.Message):
        """Is this user blocking us?"""
        try:
            await message.add_reaction("\N{gear}")
        except discord.errors.Forbidden:
            await ctx.send(f"{message.author} has me blocked!")
            return
        await message.remove_reaction("\N{gear}",self.bot.user)
        await ctx.send(f"{message.author} is not blocking me.")
        


        
        


