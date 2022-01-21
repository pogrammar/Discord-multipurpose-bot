import os
import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json
import random

with open('./data.json') as f:
    d1 = json.load(f)
with open('./market.json') as f:
    d2 = json.load(f)

nest_asyncio.apply()

mongo_url = d1['mongo']

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
ecomoney = cluster["eco"]["money"]

class Economy(commands.Cog):
    """ Commands related to economy"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Eco Cog Loaded Succesfully")

    async def open_account(self, id : int):
            newuser = {"id": id, "wallet": 0, "bank": 100}
            # wallet = current money, bank = money in bank
            await ecomoney.insert_one(newuser)

    async def update_wallet(self, id : int, wallet : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"wallet": wallet}})

    async def update_bank(self, id : int, bank : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"bank": bank}})


    @commands.command(aliases=["bal"])
    @cooldown(1, 2, BucketType.user)
    async def balance(self, ctx, user: discord.Member = None):
        """ Check your balance"""
        if user is None:
            user = ctx.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                title=f"{user}'s Balance",
                color=0xFF0000,
            )
            embed.add_field(
                name="Wallet",
                value=f"${bal['wallet']}",
            )
            embed.add_field(
                name="Bank",
                value=f"${bal['bank']}",
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
            )
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send('An error occured')

    @commands.command(aliases=["wd"])
    @cooldown(1, 2, BucketType.user)
    async def withdraw(self, ctx, amount: int):
        """ Withdraw money from your bank"""
        user = ctx.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            if amount > bal['bank']:
                await ctx.send('You do not have enough money to withdraw that much')
            elif amount <= 0:
                await ctx.send('You cannot withdraw 0 or less')
            else:
                await ecomoney.update_one({"id": user.id}, {"$inc": {"wallet": +amount, "bank": -amount}})
                await ctx.send(f'You have withdrawn ${amount}')
        except Exception:
            await ctx.send('An error occured')

    @commands.command(aliases=["dp"])
    @cooldown(1, 2, BucketType.user)
    async def deposit(self, ctx, amount: int):
        """ Deposit money to your bank"""
        user = ctx.author
        try:
            bal = await ecomoney.find_one({"id": user.id})
            if bal is None:
                await self.open_account(user.id)
                bal = await ecomoney.find_one({"id": user.id})
            if amount > bal['wallet']:
                await ctx.send('You do not have enough money to deposit that much')
            elif amount <= 0:
                await ctx.send('You cannot deposit 0 or less')
            else:
                await ecomoney.update_one({"id": user.id}, {"$inc": {"wallet": -amount, "bank": +amount}})
                await ctx.send(f'You have deposited ${amount}')
        except Exception:
            await ctx.send('An error occured')

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def rob(self, ctx, user: discord.Member = None):
        """ Rob someone"""
        if user is None or user.id == ctx.author.id:
            await ctx.send('Trying to rob yourself?')
        else:
            try:
                user_bal = await ecomoney.find_one({"id": user.id})
                member_bal = await ecomoney.find_one({"id": ctx.author.id})
                if user_bal is None:
                    await self.open_account(user.id)
                    user_bal = await ecomoney.find_one({"id": user.id})
                if member_bal is None:
                    await self.open_account(ctx.author.id)
                    member_bal = await ecomoney.find_one({"id": ctx.author.id})
                mem_bank = member_bal["bank"]
                user_bank = user_bal["bank"]
                if mem_bank < 100:
                    await ctx.send('You do not have enough money to rob someone')
                elif mem_bank >= 100:
                    if user_bank < 100:
                        await ctx.send('User do not have enough money to get robbed ;-;')
                    elif user_bank >= 100:
                        num = random.randint(1, 100)
                        f_mem = mem_bank + num
                        f_user = user_bank - num
                        await self.update_bank(ctx.author.id, f_mem)
                        await self.update_bank(user.id, f_user)
                        await ctx.send('You have robbed ${num} from {user}'.format(num=num, user=user))


            except Exception:
                await ctx.send('An error occured')

    # send money to another user
    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def send(self, ctx, user: discord.Member, amount: int):
        """ Send money to another user"""
        try:
            user_bal = await ecomoney.find_one({"id": user.id})
            member_bal = await ecomoney.find_one({"id": ctx.author.id})
            if user_bal is None:
                await self.open_account(user.id)
                user_bal = await ecomoney.find_one({"id": user.id})
            if member_bal is None:
                await self.open_account(ctx.author.id)
                member_bal = await ecomoney.find_one({"id": ctx.author.id})
            mem_bank = member_bal["bank"]
            user_bank = user_bal["bank"]
            if amount > mem_bank or amount > 20000:
                await ctx.send('You do not have enough money to send that much or amount too much')
            elif amount <= 0:
                await ctx.send('You cannot send 0 or less')
            else:
                await ecomoney.update_one({"id": ctx.author.id}, {"$inc": {"bank": -amount}})
                await ecomoney.update_one({"id": user.id}, {"$inc": {"bank": +amount}})
                await ctx.send(f'You have sent ${amount} to {user}')
        except Exception:
            await ctx.send('An error occured')

    # A economy bot fun command
    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def gamble(self, ctx, amount: int):
        """ Gamble money"""
        try:
            user_bal = await ecomoney.find_one({"id": ctx.author.id})
            if user_bal is None:
                await self.open_account(ctx.author.id)
                user_bal = await ecomoney.find_one({"id": ctx.author.id})
            if amount > user_bal["wallet"]:
                await ctx.send('You do not have enough money to gamble that much')
            elif amount <= 0:
                await ctx.send('You cannot gamble 0 or less')
            else:
                num = random.randint(1, 100)
                if num <= 50:
                    await ecomoney.update_one({"id": ctx.author.id}, {"$inc": {"wallet": +amount}})
                    await ctx.send(f'You have won ${amount}')
                elif num > 50:
                    await ecomoney.update_one({"id": ctx.author.id}, {"$inc": {"wallet": -amount}})
                    await ctx.send(f'You have lost ${amount}')
        except Exception:
            await ctx.send('An error occured')

def setup(bot):
    bot.add_cog(Economy(bot))
