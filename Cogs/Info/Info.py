
import os

import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

class Info(commands.Cog):
    """ Commands related to bot information."""
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        print("Info Cog Loaded Succesfully")

    @commands.command(aliases=["si", "serverinfo"])
    async def server(self, ctx):
        """ Info related to server"""
        own = ctx.guild.owner
        tim = str(ctx.guild.created_at)
        txt = len(ctx.guild.text_channels)
        vc = len(ctx.guild.voice_channels)
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Server Info",
            color=0xFF0000,
        )
        embed.add_field(name=":ballot_box: Name", value=f"{ctx.guild}")
        embed.add_field(name=":crown: Owner", value=f"{own.mention}")
        embed.add_field(
            name="Members",
            value=f"{ctx.guild.member_count}",
        )
        embed.add_field(name=":calendar: Created At", value=f"{tim[0:11]}")
        embed.add_field(
            name="Text Channels", value=f"{txt}"
        )
        embed.add_field(
            name="Voice Channels", value=f"{vc}"
        )
        embed.add_field(
            name="Prefix", value=f"`.`", inline=False
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["bi", "about"])
    async def bot(self, ctx):
        """ Info related to bot"""
        ser = len(self.bot.guilds)
        mem = len(self.bot.users)
        embed = discord.Embed(
            timestamp=ctx.message.created_at, title=":robot:  Bot Info", color=0xFF0000
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="Helping", value=f"{ser} servers"
        )
        embed.add_field(
            name="Serving", value=f"{mem} members"
        )
        embed.add_field(name="Prefix", value=f"`.`")
        embed.add_field(
            name="Support Server",
            value="[Join My Server](https://....)",
        )
        embed.add_field(
            name="Add Me",
            value="[Click Here to Add Me](https://....)",
        )
        embed.add_field(
            name="Website",
            value="[Checkout my website](https://....)",
        )
        embed.add_field(
            name="Made By", value="Mini.py#5183"
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["ui", "userinfo"])
    async def user(self, ctx, member: discord.Member = None):
        """ Info related to a user"""
        if member == None:
            member = ctx.author
        else:
            pass
        c = str(member.created_at)[0:11]
        j = str(member.joined_at)[0:11]
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="User Info",
            color=0xFF0000,
        )
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=":name_badge: Name", value=f"{member.name}")
        embed.add_field(
            name="Nickname", value=f"{member.nick}"
        )
        embed.add_field(name=":credit_card: Id", value=f"{member.id}")
        embed.add_field(name=":flower_playing_cards: Joined Discord", value=f"{c}")
        embed.add_field(
            name="Joined Server", value=f"{j}"
        )
        embed.add_field(
            name="Highest Role",
            value=f"{member.top_role.mention}",
        )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
