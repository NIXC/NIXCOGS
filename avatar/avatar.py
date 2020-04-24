#Credits to Yukirin#0048 for the code I based this off of.
import redbot.core
from redbot.core import commands, checks

class avatar(commands.Cog):
    """Get user's avatar URL.""" 

    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    @checks.is_owner()
    async def getavatar(self, ctx, target : int = None):
        """Gets a user's avatar. Attempts to search all guilds this bot is in. Accepts only user ID"""
        if target is None or type(target) != type(26):
            user = ctx.author
        else:
            user = self.bot.get_user(target)

        if user is None:
            try:
                user = await self.bot.fetch_user(target)
            except discord.errors.NotFound:
                pass
        
        if user is not None:
            if user.is_avatar_animated():
                url = user.avatar_url_as(format="gif")
            else:
                url = user.avatar_url_as(static_format="png")
            await ctx.send("{}'s Avatar URL : {}".format(user.name, url))
        else:
            await ctx.send(f"Unable to find user")

