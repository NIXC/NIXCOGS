import redbot.core
from redbot.core import Config, commands, checks
from redbot.core import commands
from redbot.core import checks
import re
wolAvailable = False
try:
    from wakeonlan import send_magic_packet
    wolAvailable = True
except ImportError:
    wolAvailable = False


class wol(commands.Cog):
    """wake up computers on this bots local network"""
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 166355705090146313, force_registration=True)

        default_global = dict(
            Computers={}
        )

        self.config.register_global(**default_global)

    @commands.group(name="wol")
    async def wol(self,ctx):
        """Wake up computers on this bots local network"""
        pass

    @checks.is_owner()
    @wol.command()
    async def register(self,ctx, *args):
        """Register a nickname for a particular mac address.\nUsage: wol register <Mac Address> <NickName>"""
        if len(args) != 2:
            return await ctx.send("Too many or too few arguments")
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", args[0].lower()):
            computerlist = await self.config.Computers()
            computerlist[args[1]] = args[0]
            await self.config.Computers.set(computerlist)
            return await ctx.send(f"Address {args[0]} now registered to {args[1]}")
        else:
            await ctx.send("Invalid Mac address.")

    @checks.is_owner()
    @wol.command()
    async def delete(self,ctx, nickname):
        '''Delete a nickname for a mac address'''
        computerlist = await self.config.Computers()
        if nickname != None:
            targ = computerlist.pop(nickname,None)
            if targ != None:
                await self.config.Computers.set(computerlist)
                await ctx.send(f"Nickname {targ} removed successfully")
            else:
                await ctx.send(f"{nickname} not found.")
        else:
            await ctx.send("Please enter a valid nickname to remove.")


    @checks.is_owner()
    @wol.command()
    async def wake(self,ctx,Name_or_Mac : str):
        """Wake a specified mac address, or computer"""
        if Name_or_Mac is None:
            return await ctx.send("No computer specified")
        computerlist = await self.config.Computers()
        if Name_or_Mac in computerlist:
            Name_or_Mac = computerlist.get(Name_or_Mac)
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", Name_or_Mac.lower()):
            send_magic_packet(Name_or_Mac)
            await ctx.send("Packet sent!")
        else:
            await ctx.send("Invalid Mac Address")

    @checks.is_owner()
    @wol.command(name="list")
    async def list_computers(self,ctx):
        """List all stored computer nicknames"""
        computerlist = await self.config.Computers()
        names = ""
        for name in computerlist.keys():
            names += f"{name}, "
        if len(names) > 0:
            await ctx.send(f"The following nicknames are saved: {names[0:-2]}")
        else:
            await ctx.send("No nicknames are saved")

        
        


