import discord
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']
intents = discord.Intents.all() #need to enable
bot = commands.Bot(command_prefix='~', intents=intents)

for foldername in os.listdir('./Cogs'): #for every folder in cogs
    for filename in os.listdir(f'./Cogs/{foldername}'):# for every file in a folder in cogs
        if filename.endswith('.py') and not filename in ['util.py', 'error.py']: #if the file is a python file and if the file is a cog
            bot.load_extension(f'Cogs.{foldername}.{filename[:-3]}')#load the extension



bot.run(TOKEN)
