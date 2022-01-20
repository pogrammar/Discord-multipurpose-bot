import discord
from discord.ext import commands
import os

intents = discord.Intents.all() #need to enable
bot = commands.Bot(command_prefix='~', intents=intents)

for foldername in os.listdir('./cogs'): #for every folder in cogs
    for filename in os.listdir(foldername):# for every file in a folder in cogs
        if filename.endswith('.py'): #if the file is a python file
            bot.load_extension(f'cogs.{foldername}{filename[:-3]}')#load the extension



bot.run(secrets.TOKEN)
