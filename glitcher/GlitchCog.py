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
import functools
log = logging.getLogger("red.nin.glitcher")

class GlitchCog(commands.Cog):
    """Glitches images using magic"""
    def __init__(self,bot):
        self.bot = bot
        self.glitcher = ImageGlitcher()

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def glitchavatar(self, ctx, target : Union[discord.Member,int, str] = None, glitch_amount : float = 3, glitch_change : float = 0, scan_lines : bool = False):
        """Glich a users avatar"""
        avatar = None
        if target is None:
            user = ctx.author
        elif isinstance(target, int):
            if (user := self.bot.get_user(target)) is None:
                return await ctx.send("Unable to find User")
        elif isinstance(target, discord.Member):
            user = target
        elif isinstance(target, str):
            avatar = target
            user = None
        else:
            return await ctx.send("Unable to find User")

        if glitch_amount < 0.1 or glitch_amount > 10:
            return await ctx.send("Glitch amount must be in the range (0,10]")
        if glitch_change < -10 or glitch_change > 10:
            return await ctx.send("Glitch change must be within the range [-10,10]")

        is_gif = (user and user.is_avatar_animated()) or (avatar and avatar.endswith(".gif"))
        not_gif = (user or avatar) and not is_gif

        async with ctx.channel.typing():
            if is_gif:
                if user and user.is_avatar_animated():
                    url = user.avatar_url_as(format="gif")
                else:
                    url = avatar
                img_in = await dl_image(str(url))
                imgfile = await self.exec_function(_glitch_gif, img_in, glitch_amount, glitch_change, scan_lines)
            elif not_gif:
                if user and user.is_avatar_animated():
                    url = user.avatar_url_as(format="png")
                else:
                    url = avatar
                img_in = await dl_image(str(url))
                imgfile = await self.exec_function(_glitch_still, img_in, glitch_amount, glitch_change, scan_lines)
            else:
                return await ctx.send("Invalid target")

            imgfile.seek(0)
            file_out = discord.File(imgfile)
            if imgfile.getbuffer().nbytes > (ctx.guild.filesize_limit-1024):
                log.info(f"Image too large: {imgfile.getbuffer().nbytes/1024/1024}")
                return await ctx.send("Your avatar is too powerful!")
            await ctx.send(file=file_out)



    async def exec_function(self, func, *args):
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:  #ProceedPoolExecutor is erroring for me saying No module named 'glitcher'
            return await loop.run_in_executor(pool, functools.partial(func,*args))

#Taken from TrustyJAID https://github.com/TrustyJAID/Trusty-cogs/blob/master/imagemaker/imagemaker.py
async def dl_image(url: str) -> Optional[BytesIO]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()
                return BytesIO(data)
            else:
                return None


def _glitch_gif(img_in: BytesIO, glitch_amount: float, glitch_change: float, scan_lines: bool) -> BytesIO:
    imgfile = BytesIO()
    glitcher = ImageGlitcher()
    img_in = Image.open(img_in)
    img_out, dur, frame_count  = glitcher.glitch_gif(img_in,glitch_amount, color_offset=True, glitch_change=glitch_change, scan_lines=scan_lines)
    img_out[0].save(imgfile, format="gif", save_all=True, 
            append_images=img_out[1:], duration=dur,loop=0, disposal=2, optimize=False)
    imgfile.name = "dank.gif"
    return imgfile

def _glitch_still(img_in: BytesIO, glitch_amount: float, glitch_change: float, scan_lines: bool) -> BytesIO:
    imgfile = BytesIO()
    glitcher = ImageGlitcher()
    img_in = Image.open(img_in)
    img_in = img_in.resize((512,512))
    img_out = glitcher.glitch_image(img_in,glitch_amount, color_offset=True, gif=True, frames=27, glitch_change=glitch_change, scan_lines=scan_lines)
    img_out[0].save(imgfile, format="gif", save_all=True, 
            append_images=img_out[1:], duration=60,loop=0, transparency=0, disposal=2, optimize=False)
    imgfile.name = "danker.gif"
    return imgfile
