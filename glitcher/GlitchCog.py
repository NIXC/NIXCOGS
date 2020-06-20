from functools import partial
import redbot.core
from redbot.core import Config, commands, checks
import discord
import asyncio
from io import BytesIO
from PIL import Image
from typing import Union, Optional, cast
from glitch_this import ImageGlitcher
import aiohttp
import concurrent.futures
import logging

log = logging.getLogger("red.nin.glitcher")


class GlitchCog(commands.Cog):
    """Glitches images using magic"""
    def __init__(self,bot):
        self.bot = bot
        self.glitcher = ImageGlitcher()

    #Taken from TrustyJAID https://github.com/TrustyJAID/Trusty-cogs/blob/master/imagemaker/imagemaker.py
    async def dl_image(self, url: str) -> Optional[BytesIO]:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    return BytesIO(data)
                else:
                    return None

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def glitchavatar(self, ctx, target : Union[discord.Member,int] = None, glitch_amount : float = 3, glitch_change : float = 0, scan_lines : bool = False):
        """Glich a users avatar"""
        if target is None:
            user = ctx.author
        elif isinstance(target, int):
            if (user := self.bot.get_user(target)) is None:
                return await ctx.send("Unable to find User")
        elif isinstance(target, discord.Member):
            user = target
        else:
            return await ctx.send("Unable to find User")

        if glitch_amount < 0.1 or glitch_amount > 10:
            return await ctx.send("Glitch amount must be in the range (0,10]")
        if glitch_change < -10 or glitch_change > 10:
            return await ctx.send("Glitch change must be within the range [-10,10]")
        
        async with ctx.channel.typing():
            imgfile = BytesIO()
            if user.is_avatar_animated():
                url = user.avatar_url_as(format="gif")
                img_in = Image.open(await self.dl_image(str(url)))
                img_out, dur, frame_count = await self.bot.run_in_executor(None, partial(self.glitcher.glitch_gif, img_in,glitch_amount, color_offset=True, glitch_change=glitch_change, scan_lines=scan_lines))
                img_out[0].save(imgfile, format="gif", save_all=True, 
                        append_images=img_out[1:], duration=dur,loop=0, disposal=2, optimize=False)
                imgfile.name = "dank.gif"
            else:
                url = user.avatar_url_as(static_format="png")
                img_in = Image.open(await self.dl_image(str(url)))
                img_in = img_in.resize((512,512))
                img_out = await self.bot.run_in_executor(None, partial(self.glitcher.glitch_image,img_in,glitch_amount, color_offset=True, gif=True, frames=27, glitch_change=glitch_change, scan_lines=scan_lines)
                img_out[0].save(imgfile, format="gif", save_all=True, 
                        append_images=img_out[1:], duration=60,loop=0, transparency=0, disposal=2, optimize=False)
                imgfile.name = "dank.gif"


            imgfile.seek(0)
            file_out = discord.File(imgfile)
            if imgfile.getbuffer().nbytes > 8388608:
                log.info(f"Image too large: {imgfile.getbuffer().nbytes/1024/1024}")
                return await ctx.send("Your avatar is too powerful!")
            await ctx.send(file=file_out)



