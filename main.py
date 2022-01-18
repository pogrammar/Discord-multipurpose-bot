import discord
from discord.ext import commands
from Cogs import Moderation
from Moderation import mod as mod

from Cogs import Music
from Music import music as music

from Cogs import Fun
from Music import fun as fun

intents = discord.Intents.all() #need to enable intents
bot = commands.Bot(command_prefix='~', intents=intents)

cogs1 = [mod, music, fun]

for i in range(len(cogs1)):
    cogs1[i].setup(bot)

bot.run('token')        
