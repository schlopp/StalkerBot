import discord
from discord.ext import commands

import typing
import aiohttp
import io
from PIL import Image

from cogs import _send_type

class MiscCommands(commands.Cog, name="Miscellaneous Commands"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hero', 'h'], hidden=True)
    @commands.bot_has_permissions(attach_files=True)
    async def heroify(self, ctx, ident=None, url:typing.Union[discord.User or discord.ClientUser, str]=None):

        # Send message if no ident provided
        if ident is None:
            return await ctx.send("You didn't provide a valid heroify identifier (h, H, A, l)")

        # Decide what type of H to use
        try:
            h_type = {
                "h": 'images/cursive_hero_h.png', # Cursive H
                "H": 'images/hero_h.png', # Normal H
                "A": 'images/aiko_a.png', # Aiko A
                "l": 'images/lemon.png' # Lemon
            }[ident[0]]
        except KeyError:
            return await ctx.send("You didn't provide a valid heroify identifier (h, H, A, l)")

        # Check if the image should be a user PFP
        if isinstance(url, discord.User):
            url = str(url.avatar_url_as(format="png"))

        # Set the image URL to the message attachment link if it's None
        if url is None:
            if len(ctx.message.attachments) > 0:
                url = ctx.message.attachments[0].url
            else:
                return await ctx.send("You didn't provide a valid image URL")

        # Get the data from the url
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                image_bytes = await r.read()

        # "Hey python, treat this as a file so you can open it later"
        image_file = io.BytesIO(image_bytes)

        # Assign variables for the images (the image sent by user and the H)
        base_image = Image.open(image_file)
        h_image = Image.open(h_type)

        # Resize the base image to be the same size as the H
        base_image = base_image.resize(h_image.size)

        # Add an H to the base image
        base_image.paste(h_image, (0, 0), h_image)

        # Change the base image back to bytes so we can send it to Discord
        sendable_image = io.BytesIO()
        base_image.save(sendable_image, "PNG")
        sendable_image.seek(0)

        await ctx.send(file=discord.File(sendable_image, filename="heroed.png"))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def send(self, ctx, channel_type:typing.Optional[_send_type], snowflake:typing.Union[discord.User, discord.TextChannel, int], *, message:str):
        """Sends a message to a channel or a user through StalkerBot"""

        # Hopefully `snowflake` is a Discord object, but if it's an int we should try getting it
        if type(snowflake) is int:
            method = {
            "c": self.bot.get_channel,
            "u": self.bot.get_user,
            }[channel_type[0]]
            snowflake = method(snowflake)

        # And send
        await snowflake.send(message)

        # React to the command message
        await ctx.message.add_reaction("👌")
        
    @commands.command(hidden=True)
    async def react(self, ctx, messageid, reaction="okay"):
        """Reacts to a message in a channel with a reaction"""

        try:
            reaction = { # Preset reactions
                "okay": "👌",
                "up": "👍",
                "down": "👎",
            }[reaction.lower()]
        except KeyError:
            reaction = reaction

        message = await ctx.channel.fetch_message(messageid)
        await message.add_reaction(reaction)


def setup(bot):
    bot.add_cog(MiscCommands(bot))