from . import resmon, psutilAvailable

def setup(bot):
    if psutilAvailable:
        bot.add_cog(resmon(bot))
    else:
        raise RuntimeError("Need to run pip install psutil")