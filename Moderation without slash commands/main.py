import discord
from discord.ext import commands
import discord.ui
from discord.ui import *

intents = discord.Intents.all() #need to enable intents
bot = commands.Bot(command_prefix='~', intents=intents)

class Moderation(commands.Cog):
	def __init__(self, bot):
        self.bot = bot


    @bot.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(ctx, amount: int):
        await ctx.channel.purge(limit = amount)
        await ctx.send("Done.")
    @bot.command()
    @commands.has_permissions(kick_members = True)
    async def kick(ctx,  member: discord.Member):
    
        await member.kick(reason=None)   
        await ctx.send("Done.")
    @bot.command()
    @commands.has_permissions(ban_members = True)
    async def ban(ctx, member: discord.Member):
    
        await member.ban(reason=None, delete_message_days=0)   
        await ctx.send("Done.")    
    @bot.command()
    @commands.has_permissions(ban_members = True)
    async def unban(ctx, member : discord.Member):
    
        await member.unban(member, reason=None)   
        await ctx.respond("Done.")
    
    @bot.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(ctx, member: discord.Member):
        muted_role = ctx.guild.get_role(MUTED_ROLE_ID)
    
        await member.add_roles(muted_role)
    
        await ctx.send("The member has been muted")
    @bot.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(ctx, member: discord.Member):
        muted_role = ctx.guild.get_role(MUTED_ROLE_ID)
    
        await member.remove_roles(muted_role)
    
        await ctx.send("The member has been unmuted")                                                   
                                                 

    @bot.command()
    async def membercount(ctx):
        await ctx.send(ctx.guild.member_count)
	
    @bot.command()
    async def timeout(ctx, member: discord.Member, minutes: int):
        """Apply a timeout to a member"""

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)
        await ctx.reply(f"Member timed out for {minutes} minutes.")	

bot.add_cog(Moderation(bot))
bot.run('token')        
