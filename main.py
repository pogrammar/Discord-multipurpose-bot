import discord
from discord.ext import commands
from Cogs import mod as mod

intents = discord.Intents.all() #need to enable intents
bot = commands.Bot(command_prefix='~', intents=intents)

cogs1 = [mod]

for i in range(len(cogs1)):
    cogs1[i].setup(bot)

bot.run('token')        
