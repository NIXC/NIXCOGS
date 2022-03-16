import redbot.core
from redbot.core import Config, commands, checks
import discord

import logging
from redbot.core.data_manager import cog_data_path
import os
import subprocess
import re

log = logging.getLogger("red.nin.rusthon")

CODE_BLOCK_RE = re.compile(r"^((```rust)(?=\s)|(```))")
class rusthon(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.initialized = os.path.isfile(cog_data_path(self)/"internalproj"/"Cargo.toml")

    def subprocessrun(self, args):
        """Helper Function that contains all the needed arguments"""
        return subprocess.run(args,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cog_data_path(self)/"internalproj")

    def cleaninput(self, code):
        """Shamelessly stolen/modified from redbot's dev command"""
        if(code.startswith("```") and code.endswith("```")):
            return CODE_BLOCK_RE.sub("", code)[:-3]

        return code.strip("` \n")

    @commands.command()
    @checks.is_owner()
    async def rustinit(self, ctx):
        if not os.path.isfile(cog_data_path(self)/"internalproj"/"Cargo.toml"):
            subrun = subprocess.run(["cargo", "new", cog_data_path(self)/"internalproj"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if len(subrun.stdout):
                await ctx.send(f"```{subrun.stdout}```")
            if len(subrun.stderr):
                await ctx.send(f"```{subrun.stderr}```")
            if subrun.returncode == 0:
                self.initialized = True
        else:
            self.initialized = True
    
    @commands.command()
    @checks.is_owner()
    async def rusteval(self,ctx, *, body: str):
        if not self.initialized:
            return
        body = self.cleaninput(body)
        if "fn main()" not in body:
            #We need to wrap the code in a main function
            body = f"fn main(){{\n{body}\n}}"

        with open(cog_data_path(self)/"internalproj"/"src"/"main.rs", "w") as outputfile:
            outputfile.write(body)
        compilerrun = self.subprocessrun(["cargo", "build"])
        if len(compilerrun.stdout):
            await ctx.send(f"```{compilerrun.stdout}```")
        if len(compilerrun.stderr):
            cleaned = compilerrun.stderr.replace(f"({str(cog_data_path(self)/'internalproj')})", '')
            await ctx.send(f"```{cleaned}```")
        if compilerrun.returncode != 0:
            return await ctx.send("Failed to execute...")

        progrun = subprocess.run([cog_data_path(self)/"internalproj"/"target"/"debug"/"internalproj"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if len(progrun.stdout):
            await ctx.send(f"```{progrun.stdout}```")
        if len(progrun.stderr):
            await ctx.send(f"```{progrun.stderr}```")


