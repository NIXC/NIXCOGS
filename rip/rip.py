import discord
import os
from redbot.core import commands
from redbot.core import checks
from redbot.core import data_manager
from typing import Optional
from io import BytesIO
import logging

log = logging.getLogger("red.NIXCOGS.rip")


try:
    import PIL
    pillowAvailable = True
    from PIL import Image
except ImportError:
    pillowAvailable = False

BaseCog = getattr(commands, "Cog", object)

class rip(BaseCog):
    """Put someones face on a tombstone"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def rip(self, ctx, member: discord.Member = None, words: Optional[str] = ""):
        """Put someones face on a tombstone"""

        path = data_manager.bundled_data_path(self)


        image = Image.open(os.path.join(path,"dumbstone.png"))

        data = BytesIO()
        data.name = "rip.png"
        image.save(data)
        data.seek(0)

        await ctx.send(file=discord.File(data))

        
