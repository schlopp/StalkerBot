import discord
from discord.ext import commands
import voxelbotutils as utils


class SchloppCog(utils.Cog, name="SchloppShowingHisLove"):

    def __init__(self, bot):
        self.bot = bot
    
    async def preform_action(self, ctx, description:str):
        """Preform a verified gangster schlöpp action"""
        
        #Dont want everyone using this.
        if ctx.author.id != 393305855929483264 and ctx.author.id != 322542134546661388:
            return
        
        with utils.Embed(use_random_colour=True) as embed:
            embed.description = description
        
        await ctx.send(embed=embed)

    @utils.command(hidden=True)    
    async def takegeorgeoutfordinner(self, ctx):
        """Takes george out to dinner"""
        
        await preform_action(ctx,"You take george out for a nice, romantic date in a fancy restaurant.")
    
    @utils.command(hidden=True)    
    async def kissgeorge(self, ctx):
        """Takes george out to dinner"""
        
        await preform_action(ctx, "You step out of the restaurant with george. While walking back to his place, you feel like the time is right and kiss him.")


def setup(bot):
    bot.add_cog(SchloppCog(bot))
