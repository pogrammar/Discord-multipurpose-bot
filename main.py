import discord
from discord.ext import commands
import os


for foldername in os.listdir('./cogs'):
    for filename in os.listdir(foldername):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{foldername}{filename[:-3]}')

intents = discord.Intents.all() #need to enable intents in discord dev portal
bot = commands.Bot(command_prefix='~', intents=intents)

bot.run('token')        
