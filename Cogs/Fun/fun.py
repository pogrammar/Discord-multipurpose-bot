import random
from random import random

import discord
from discord.ext import commands
from discord.commands import Option  #Importing the packages
from discord.commands import slash_command


class Fun(commands.Cog):
    def __init__(self, bot):#to Initialise
        self.bot = bot

    @slash_command(guild_ids=[...])
    async def eightball(self, ctx, question: Option(str)):
        ballresponse = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;","i think....","gg","I-\ndont know what to say"
        ]

        answer = random.choice(ballresponse)
        await ctx.respond(f"🎱 **Question:** {question}\n**Answer:** {answer}")
    
    @slash_command(guild_ids=[...])
    async def hotcalc(self, ctx, user: Option(discord.Member)):    
        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"    

        await ctx.respond(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")            

def setup(bot):
    bot.add_cog(Fun(bot))        
