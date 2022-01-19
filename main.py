import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='~', intents=intents)
intents = discord.Intents.all() #need to enable intents in discord dev portal

for foldername in os.listdir('./cogs'):
    for filename in os.listdir(foldername):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{foldername}{filename[:-3]}')



bot.run('token')        
