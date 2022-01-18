import discord
from discord.ext import commands
from discord.commands import Option  #Importing the packages
import discord.ui
from discord.ui import *
import datetime

intents = discord.Intents.all() #need to enable intents
bot = commands.Bot(command_prefix='~', intents=intents)


class Moderation(commands.Cog)
	def __init__(self, bot):#to Initialise
        self.bot = bot


    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(manage_messages = True)
    async def clear(ctx, amount: Option(int, "Member")):    
        await ctx.channel.purge(limit = amount)#Get the channel where the command is executed, then purge no. of messages provided
        await ctx.respond("Done.")#respond because in slash commands the response shows a little reply thing on top, for that you need ctx.respond


    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(kick_members = True)
    async def kick(ctx,  member: Option(discord.Member, "Member")):
    
        await member.kick(reason=None)#kick th member with no reason. you can add another option with "str" as the first param   
        await ctx.respond("Done.")


    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(ban_members = True)
    async def ban(ctx, member: Option(discord.Member, "Member")):
    
        await member.ban(reason=None, delete_message_days=0)#ban and dont delete any messages
        await ctx.respond("Done.")    


    @bot.command()#Because unban doesnt work with slash commands
    @commands.has_permissions(ban_members = True)
    async def unban(ctx, member : discord.Member):
    
        await member.unban(member, reason=None)
        await ctx.respond("Done.")
    
    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(manage_roles = True)
    async def mute(ctx, member: Option(discord.Member, "Member")):
        muted_role = ctx.guild.get_role(MUTED_ROLE_ID)#get the muted role with ID
    
        await member.add_roles(muted_role)#add the mute role
    
        await ctx.respond("The member has been muted")


    @bot.slash_command(guild_ids=[...])
    @commands.has_permissions(manage_roles = True)
    async def unmute(ctx, member: Option(discord.Member, "Member")):
        muted_role = ctx.guild.get_role(MUTED_ROLE_ID)
    
        await member.remove_roles(muted_role)#remove muted role
    
        await ctx.respond("The member has been unmuted")                                                   
                                                 

    @bot.slash_command(guild_ids=[...])
    async def membercount(ctx):
        await ctx.respond(ctx.guild.member_count)#get guild no. of members
	
    @bot.slash_command(guild_ids=[...])
    async def timeout(ctx, member: Option(discord.Member, "Member"), minutes: Option(int, "Minutes")):
        """Apply a timeout to a member"""

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)#timeout for the amount of time given, then remove timeout
        await ctx.reply(f"Member timed out for {minutes} minutes.")	


bot.add_cog(Moderation(bot))
bot.run('token')        
