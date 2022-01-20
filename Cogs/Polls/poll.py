import discord
from discord.ext import commands, ui
from discord.commands import Option
from discord.commands import slash_command
from discord.ui import button

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[...])
    async def poll(ctx,
                   question: Option(str),
                   a: Option(str),
                   b: Option(str)):
        embed = discord.Embed(title=question,
                              description=f"🅰️: {a}\n 🅱️: {b}")
        await ctx.respond(embed=embed)
        msg = await ctx.interaction.original_message()
        await msg.add_reaction('🅰️')
        await msg.add_reaction('🅱️')

def setup(bot):
    bot.add_cog(Poll(bot))
