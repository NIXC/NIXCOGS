from wakeonlan import send_magic_packet
from wol.wol import wol, wolAvailable

def setup(bot):
    if wolAvailable:
        bot.add_cog(wol(bot))
    else:
        raise RuntimeError("Need to run pip install wakeonlan")