import discord
from discord.ext import commands


from Cogs.Fun import fun
from Cogs.Info import Info
from Cogs.Moderation import mod
from Cogs.Music import music
from Cogs.Paginator import Paginator
from Cogs.tictactoe import tic_tac_toe

intents = discord.Intents.all() #need to enable intents in discord dev portal
bot = commands.Bot(command_prefix='~', intents=intents)


cogs1 = [fun, Info, mod, music, Paginator, tic_tac_toe]

for i in range(len(cogs1)):
    cogs1[i].setup(bot)

bot.run('token')        
