import discord
from discord.ext import commands
import cogs.mod as mod

intents = discord.Intents.all() #need to enable intents
bot = commands.Bot(command_prefix='~', intents=intents)

cogs = [mod]

for i in range(len(cogs)):
    cogs[i].setup(bot)


bot.run('token')        
