from rip.rip import rip, pillowAvailable

def setup(bot):
    if pillowAvailable:
        bot.add_cog(rip(bot))
    else:
        raise RuntimeError("Need to run 'pip install pillow'. You may also need to install libjpeg-dev")