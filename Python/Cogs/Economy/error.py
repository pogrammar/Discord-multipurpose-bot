import math
import os
import sys
import traceback

import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Error cog loaded successfully")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        # get the original exception
        error = getattr(error, "original", error)

        if isinstance(error, commands.BotMissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)

            embed = discord.Embed(
                title="Missing Permissions",
                description=f"I am missing **{fmt}** permissions to run this command :(",
                color=0xFF0000,
            )
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send("This command has been disabled.")
            return

        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Cooldown",
                description=f"This command is on cooldown, please retry in {math.ceil(error.retry_after)}s.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.MissingPermissions):
            missing = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in error.missing_perms
            ]
            if len(missing) > 2:
                fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = " and ".join(missing)
            embed = discord.Embed(
                title="Insufficient Permission(s)",
                description=f"You need the **{fmt}** permission(s) to use this command.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.UserInputError):
            embed = discord.Embed(
                title="Invalid Input",
                description=f"Maybe you forgot to specify inputs or gave an extra input",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This command cannot be used in direct messages.")
            except discord.Forbidden:
                raise error
            return
        if isinstance(error, discord.errors.Forbidden):
            try:
                embed = discord.Embed(
                    title="Forbidden",
                    description=f"Error - 403 - Forbidden | Missing perms",
                    color=0xFF0000,
                )
                await ctx.send(embed=embed)
            except:
                print("Failed forbidden")
            return

        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Permissions Not Satisfied",
                description=f"You do not have permissions to use this command",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
            return

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)

        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )


def setup(bot):
    bot.add_cog(Errors(bot))
