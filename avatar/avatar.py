#Credits to Yukirin#0048 for the code I based this off of.
import redbot.core
from redbot.core import commands

class avatar(commands.Cog):
    """Get user's avatar URL.""" 

    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def avatar(self, ctx, target):
        """Gets a user's avatar. Attempts to search all guilds this bot is in. Accepts only user ID"""
        if target is None or type(target) != type(26):
            user = ctx.author
        else:
            for guild in self.bot.guilds:
                user = guild.get_member(target)
                if user is not None:
                    break

        if user is not None:
            if user.is_avatar_animated():
                url = user.avatar_url_as(format="gif")
            else:
                url = user.avatar_url_as(static_format="png")
            await ctx.send("{}'s Avatar URL : {}".format(user.name, url))
        else:
            await ctx.send(f"Unable to find user")

