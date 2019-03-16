
try:
    import psutil
    psutilAvailable = True
except ImportError:
    psutilAvailable = False

BaseCog = getattr(commands, "Cog", object)
class resmon(BaseCog):
    """Record system information about the server running this instance"""
    def __init__(self, bot):
        self.bot = bot
