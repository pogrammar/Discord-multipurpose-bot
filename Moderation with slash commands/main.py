import discord
from discord.ext import commands
from discord.commands import Option
import discord.ui
from discord.ui import *

intents = discord.Intents.all() #need to enable intents
bot = commands.Bot(command_prefix='~', intents=intents)

class Moderation(commands.Cog):
	def __init__(self, bot):
        self.bot = bot


    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(manage_messages = True)
    async def clear(ctx, amount: Option(int, "Member")):    
        await ctx.channel.purge(limit = amount)
        await ctx.respond("Done.")
    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(kick_members = True)
    async def kick(ctx,  member: Option(discord.Member, "Member")):
    
        await member.kick(reason=None)   
        await ctx.respond("Done.")
    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(ban_members = True)
    async def ban(ctx, member: Option(discord.Member, "Member")):
    
        await member.ban(reason=None, delete_message_days=0)   
        await ctx.respond("Done.")    
    @bot.command()#Because unban doesnt work with slash commands
    @commands.has_permissions(ban_members = True)
    async def unban(ctx, member : discord.Member):
    
        await member.unban(member, reason=None)   
        await ctx.respond("Done.")
    
    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(manage_roles = True)
    async def mute(ctx, member: Option(discord.Member, "Member")):
        muted_role = ctx.guild.get_role(MUTED_ROLE_ID)
    
        await member.add_roles(muted_role)
    
        await ctx.respond("The member has been muted")
    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(manage_roles = True)
    async def unmute(ctx, member: Option(discord.Member, "Member")):
        muted_role = ctx.guild.get_role(MUTED_ROLE_ID)
    
        await member.remove_roles(muted_role)
    
        await ctx.respond("The member has been unmuted")                                                   
                                                 

    @bot.slash_command(guild_ids=[...])
    async def membercount(ctx):
        await ctx.respond(ctx.guild.member_count)


bot.add_cog(Moderation(bot))
bot.run('token')        
