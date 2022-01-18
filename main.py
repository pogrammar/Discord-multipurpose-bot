import discord
from discord.ext import commands
from Cogs import Moderation
from Moderation import mod as mod

from Cogs import Music
from Music import music as music

from Cogs import Info
from Info import Info as Info#from cogs folder get Info folder --> from Info folder get Info.py as Info

from Cogs import Fun
from Music import fun as fun



intents = discord.Intents.all() #need to enable intents in discord dev portal
bot = commands.Bot(command_prefix='~', intents=intents)


cogs1 = [mod, music, fun, Info]

for i in range(len(cogs1)):
    cogs1[i].setup(bot)

bot.run('token')        
