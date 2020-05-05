#Credits to Yukirin#0048 for the code I based this off of.
import redbot.core
import discord
from typing import Union, Optional, cast
from redbot.core import commands, checks

class avatar(commands.Cog):
    """Get user's avatar URL.""" 

    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    @checks.is_owner()
    async def getavatar(self, ctx, target : Union[discord.Member,int,str] = None):
        """Gets a user's avatar. Accepts typed names, or an ID. Will fetch an ID not in the server."""
        if target is None:
            user = ctx.author
        elif isinstance(target, int):
            if (user := self.bot.get_user(target)) is None:
                try:
                    user = await self.bot.fetch_user(target)
                except discord.errors.NotFound:
                    return await ctx.send("Unable to find User")
        elif isinstance(target, discord.Member):
            user = target
        else:
            return await ctx.send("Unable to find User")

        if user.is_avatar_animated():
            url = user.avatar_url_as(format="gif")
        else:
            url = user.avatar_url_as(static_format="png")
        await ctx.send("{}'s Avatar URL : {}".format(user.name, url))

