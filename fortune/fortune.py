import discord
from redbot.core import checks, commands
import subprocess
import asyncio
from subprocess import Popen
import threading
from asyncio.subprocess import PIPE, STDOUT
from redbot.core.utils.chat_formatting import pagify
#from redbot.core.config import Config
import random

BaseCog = getattr(commands, "Cog", object)

class Fortune(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.cowsay = ['cowsay','cowthink']
        self.normal = ['default']
        self.cows = ['default','cower','moofasa','moose','pony-smaller','sheep','skeleton','www','three-eyes','pony-smaller']
        self.animals = ['apt','bunny','duck','elephant','flaming-sheep','hellokitty','koala','luke-koala','suse','tux','unipony-smaller','vader','vader-koala']

        #self.config = Config.get_conf(self, identifier=166355705090146313, force_registration=True)
    
    def getanimal(self):
        num = random.randint(0,100)
        if num < 60:
            return random.choice(self.normal)
        if num < 90:
            return random.choice(self.cows)
        return random.choice(self.animals)

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def fortune(self, ctx):
        """Get a fortune"""
        await self.send_fortunes(ctx,"fortunes goedel")

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def riddle(self, ctx):
        """Get a riddle"""
        await self.send_fortunes(ctx,"75% riddles 25% paradoxum")

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def disclaimer(self, ctx):
        """Get a disclaimer"""
        await self.send_fortunes(ctx,"disclaimer")

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def bofh(self, ctx):
        """I wonder what the operators excuse is this time?"""
        await self.send_fortunes(ctx,"bofh-excuses")

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def zippy(self, ctx):
        """It's an absolutely abstract kind of real cancer in here."""
        await self.send_fortunes(ctx,"zippy")

    #Credits to Grande for bash cog, which this basically reuses but totally differently.
    async def send_fortunes(self, ctx, kind):
        proc = await asyncio.create_subprocess_shell(f"/usr/games/fortune {kind} |tr -d '\\t' | /usr/games/{random.choice(self.cowsay)} -f {self.getanimal()}", stdin=None, stderr=STDOUT, stdout=PIPE)
        out = await proc.stdout.read()
        msg = pagify(out.decode('utf-8'))
        await ctx.send_interactive(msg, box_lang="")

