import discord
from discord.ext import commands
from discord.commands import Option  #Importing the packages
import datetime
from discord.commands import slash_command


class Info(commands.Cog):
    def __init__(self, bot):#to Initialise
        self.bot = bot

    @slash_command()
    async def userinfo(self, ctx, user: Option(discord.Member)): # b'\xfc'  
        date_format = "%a, %d %b %Y %I:%M %p"

        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))

        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)


        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])

        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.respond(embed=embed)    

def setup(bot):
    bot.add_cog(Info(bot))        
