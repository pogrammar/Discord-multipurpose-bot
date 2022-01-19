import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option  #Importing the packages
import datetime
import json


class Moderation(commands.Cog):
    def __init__(self, bot):#to Initialise
        self.bot = bot


    @slash_command(guild_ids=[...])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount: Option(int)):    
        await ctx.channel.purge(limit = amount)#Get the channel where the command is executed, then purge no. of messages provided
        await ctx.respond("Done.")#respond because in slash commands the response shows a little reply thing on top, for that you need ctx.respond
    
    
    @slash_command(guild_ids=[...])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx,  member: Option(discord.Member)):
    
        await member.kick(reason=None)#kick th member with no reason. you can add another option with "str" as the first param   
        await ctx.respond("Done.")
    
    
    @slash_command(guild_ids=[...])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: Option(discord.Member)):
    
        await member.ban(reason=None, delete_message_days=0)#ban and dont delete any messages
        await ctx.respond("Done.")    


    @commands.command()#Because unban doesnt work with slash commands
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member : discord.Member):
    
        await member.unban(member, reason=None)
        await ctx.respond("Done.")
    
    @slash_command(guild_ids=[...])
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member: Option(discord.Member)):
        muted_role = ctx.guild.get_role(1234567890)#get the muted role with ID
    
        await member.add_roles(muted_role)#add the mute role
    
        await ctx.respond("The member has been muted")


    @slash_command(guild_ids=[...])
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member: Option(discord.Member)):
        muted_role = ctx.guild.get_role(1234567890)
    
        await member.remove_roles(muted_role)#remove muted role
    
        await ctx.respond("The member has been unmuted")                                                   
                                                 

    @slash_command(guild_ids=[...])
    async def membercount(self, ctx):
        await ctx.respond(ctx.guild.member_count)#get guild no. of members
	
    @slash_command(guild_ids=[...])
    async def timeout(self, ctx, member: Option(discord.Member), minutes: Option(int)):
        """Apply a timeout to a member"""

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)#timeout for the amount of time given, then remove timeout
        await ctx.reply(f"Member timed out for {minutes} minutes.")	


#Warn command section(it is still in the same class)-----------------------------------------------------

    @slash_command(guild_ids=[...])    
    async def warnings(self, ctx, member: Option(discord.Member)):
        await self.open_account(member)

        users = await self.get_user_data()

        warns = users[str(member.id)]["warns"]

        await ctx.respond(f"{member.name} has {warns} warns.")

    @slash_command(guild_ids=[...])    
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member: Option(discord.Member)):
        await self.open_account(member)

        users = await self.get_user_data()

        warns = await self.warn(member)

        await ctx.respond(f"<@{member.id}> has been warned. They now have {warns} warns.")
	
	
    async def open_account(self, user):
        with open ("./Cogs/Moderation/reports.json","r")as f:
            users = json.load(f)
        if str (user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["warns"] = 0
        
        with open("./Cogs/Moderation/reports.json","w")as f:
            json.dump(users, f)
	
	
    async def get_user_data(self):
        with open ("./Cogs/Moderation/reports.json","r")as f:
            users = json.load(f)
        return users


    async def warn(self, user, change = 1, mode = "warns"):
        users = await self.get_user_data()
    
        users[str(user.id)][mode] += change
    
        with open("./Cogs/Moderation/reports.json","w")as f:
            json.dump(users, f)
        
        warns = users[str(user.id)][mode]
    
        return warns	

def setup(bot):
    bot.add_cog(Moderation(bot))
