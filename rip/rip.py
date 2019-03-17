import discord
import os
from redbot.core import commands
from redbot.core import checks
from redbot.core import data_manager
from typing import Optional, Union
from io import BytesIO
import logging
import aiohttp

log = logging.getLogger("red.NIXCOGS.rip")


try:
    import PIL
    pillowAvailable = True
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    pillowAvailable = False

BaseCog = getattr(commands, "Cog", object)

class rip(BaseCog):
    """Put someone's face on a tombstone"""
    def __init__(self, bot):
        self.bot = bot

    def get_avatar_url(url):
        if ".gif" in url:
            return url.split('.gif')[0] + ".png?size=2048"
        else:
            return url.split('.webp')[0] + ".png?size=2048"

    #stolen from https://github.com/Flame442/FlameCogs/tree/dev/deepfry
    async def _get_image(self,ctx,link):   
        async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    r = await response.read()
                    try:
                        img = Image.open(BytesIO(r))
                    except:
                        raise ValueError('An image could not be found. Make sure you provide a direct link.')
        return img

    def generate_mugshot(self,img,mask):
        img = img.resize((256,256))
        mask = mask.getchannel("A")
        img.putalpha(mask)

        return img

    def insert_face(self,face,stone):
        left = 432
        top = 237
        right = left + 256
        bottom = top + 256
        #face = face.rotate(-9)
        stone.paste(face,(left,top,right,bottom),face)
        return stone

    def insert_words(self,words,stone):
        draw = ImageDraw.Draw(stone)
        font = ImageFont.truetype("FreeMono.ttf", 62, encoding="unic")
        draw.text((125, 520), words,'black', font=font)
        return stone


    @commands.command()
    async def rip(self, ctx, member: Optional[discord.Member] = None, *words):
        """Put someone's face on a tombstone"""
        path = data_manager.bundled_data_path(self)


        image = Image.open(os.path.join(path,"dumbstone.png"))
        mask = Image.open(os.path.join(path,"mugshot.png"))
        avatar = member.avatar_url
        try:
            img = await self._get_image(ctx,rip.get_avatar_url(avatar))
        except ValueError as error:
            await ctx.send(error)
            return

        data = BytesIO()

        img = self.generate_mugshot(img,mask)
        img = self.insert_face(img,image)
        #this is bad and I should feel bad
        if len(words) > 0:
            out = ""
            count = 0
            for word in words:
                out += word + " "
                if len(out) > 24+count*24:
                    out += "\n"
                    count += 1
            img = self.insert_words(out,img)

        img.save(data,"PNG")
        data.seek(0)
        data.name = "rip.png"
        await ctx.send(file=discord.File(data))

        
