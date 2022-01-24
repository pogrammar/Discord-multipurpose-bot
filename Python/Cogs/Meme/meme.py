import discord
from discord import Embed
from discord.ext import commands
import asyncpraw
import random


class Meme(commands.Cog):
    def __init__(self, bot):#to Initialise
        self.bot = bot
    
    @commands.command()
    async def meme(self, ctx, subred="memes"): # default subreddit is memes, later in the command you can select one of your choice (example: !meme python --> chooses r/python reddit post)
        msg = await ctx.send('Loading ... ')

        reddit = asyncpraw.Reddit(client_id='clientid',
                                  client_secret='clientsecret',
                                  username='username',
                                  password='password',
                                  user_agent='useragent')

        subreddit = await reddit.subreddit(subred)
        all_subs = []
        top = subreddit.top(limit=250) # bot will choose between the top 250 memes

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = Embed(title=f'__{name}__', colour=discord.Colour.random(), timestamp=ctx.message.created_at, url=url)

        embed.set_image(url=url)
        embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        embed.set_footer(text='Here is your meme!')
        await ctx.send(embed=embed)
        await msg.edit(content=f'<https://reddit.com/r/{subreddit}/> :white_check_mark:') # < and > remove the embed link
        return

def setup(bot):
    bot.add_cog(Meme(bot))   
