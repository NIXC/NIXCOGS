from redbot.core import commands
from redbot.core import checks

psutilAvailable = False
try:
    import psutil
    psutilAvailable = True
except ImportError:
    psutilAvailable = False


class resmon(commands.Cog):
    """Record system information about the server running this instance"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="resmon")
    async def resmon(self,ctx):
        """Record system information about the server running this instance"""
        pass

    

if __name__ == "__main__":
    print("hi")
    print(psutilAvailable)