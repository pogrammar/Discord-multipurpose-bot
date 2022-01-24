import google
from googlesearch import search
import discord
from discord.ext import commands
from discord.commands import Option  #Importing the packages
import datetime
from discord.commands import slash_command

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[...])
    async def search(self, ctx, query: Option(str)):
        msg = await ctx.respond(f"Searching...🔍")
        embed = discord.Embed(title=f"Search results", description=f"Query: {query}")
        for j in search(query, num=5, stop=5, pause=2):#increase num and stop for the amount of results you want
            embed.add_field(name="Search result:", value=j)
        await msg.edit(embed=embed)



def setup(bot):
    bot.add_cog(Search(bot))

