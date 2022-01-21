import os
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import motor.motor_asyncio
import nest_asyncio
import json

with open('./data.json') as f:
    d1 = json.load(f)
with open('./market.json') as f:
    d2 = json.load(f)

items = {}

for x in d2["IoT"]:
    i = {x[2] : ["iot", x[1], x[0]]}    
    items.update(i)

for x in d2["Food"]:
    i = {x[2] : ["food", x[1], x[0]]}
    items.update(i)

for x in d2["Cars"]:
    i = {x[2] : ["cars", x[1], x[0]]}
    items.update(i)

#print(items)

nest_asyncio.apply()

mongo_url = d1['mongo']

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
ecomoney = cluster["eco"]["money"]
ecobag = cluster["eco"]["bag"]

class Shop(commands.Cog):
    """ Commands related to market"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Shop Cog Loaded Succesfully")


    async def open_account(self, id : int):
        if id is not None:
            newuser = {"id": id, "wallet": 0, "bank": 100}
            # wallet = current money, bank = money in bank
            await ecomoney.insert_one(newuser)

    async def update_wallet(self, id : int, wallet : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"wallet": wallet}})

    async def update_bank(self, id : int, bank : int):
        if id is not None:
            await ecomoney.update_one({"id": id}, {"$set": {"bank": bank}})

    async def open_bag(self, id : int):
        if id is not None:
            newuser = {"id": id, "bag": []}
            await ecobag.insert_one(newuser)


    @commands.group(name="mkt", invoke_without_command=True)
    @cooldown(1, 2, BucketType.user)
    async def mkt(self,ctx):
        """ Market Commands"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Market Categories",
            color=0xFF0000,
        )
        embed.add_field(
            name="IoT",
            value="Buy items related to IoT/Technology | Use `.mkt iot`",
            inline=False
        )
        embed.add_field(
            name="Food",
            value="Buy items related to Food | Use `.mkt food`",
            inline=False
        )
        embed.add_field(
            name="Cars",
            value="Buy items related to Cars | Use `.mkt cars`",
            inline=False
        )
        embed.set_footer(
        text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )

        await ctx.send(embed=embed)

    @mkt.command(name="iot")
    @cooldown(1, 2, BucketType.user)
    async def iot(self,ctx):
        """ IoT/Technology Market"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="IoT Market",
            color=0xFF0000,
        )
        for x in d2["IoT"]:
            embed.add_field(
                name=x[0],
                value=f"Name {x[2]} | Price: ${x[1]}",
                inline=False
            )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    @mkt.command(name="food")
    @cooldown(1, 2, BucketType.user)
    async def food(self,ctx):
        """ Food Market"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Food Market",
            color=0xFF0000,
        )
        for x in d2["Food"]:
            embed.add_field(
                name=x[0],
                value=f"Name {x[2]} | Price: ${x[1]}",
                inline=False
            )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    @mkt.command(name="cars")
    @cooldown(1, 2, BucketType.user)
    async def cars(self,ctx):
        """ Cars Market"""
        embed = discord.Embed(
            timestamp=ctx.message.created_at,
            title="Automobile Market",
            color=0xFF0000,
        )
        for x in d2["Cars"]:
            embed.add_field(
                name=x[0],
                value=f"Name {x[2]} | Price: ${x[1]}",
                inline=False
            )
        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    # function to add item in ecobag
    async def add_item(self, id : int, item : str, amount : int):
        if id is not None:
            await ecobag.update_one({"id": id}, {"$push": {"bag": [item, amount]}})
        
    # function to edit amount of item in ecobag
    async def edit_item(self, id : int, index : int, amount : int):
        if id is not None:
            await ecobag.update_one({"id": id}, {"$set": {f"bag.{index}.1": amount}})

    # function to remove item from ecobag
    async def remove_item(self, id : int, name : str, amount : int):
        if id is not None:
            await ecobag.update_one({"id": id}, {"$pull": {"bag": [name, amount]}})


    @commands.command(aliases=["b"])
    @cooldown(1, 2, BucketType.user)
    async def buy(self, ctx, item : str, amount : int = 1):
        """ Buy an item from the market"""
        if amount <= 0 or amount > 100:
            await ctx.send("Amount must be greater than 0 or less than 100")
            return
        bal = await ecomoney.find_one({"id": ctx.author.id})
        if bal is None:
            await self.open_account(ctx.author.id)
            bal = await ecomoney.find_one({"id": ctx.author.id})

        bag = await ecobag.find_one({"id": ctx.author.id})
        if bag is None:
            await self.open_bag(ctx.author.id)
            bag = await ecobag.find_one({"id": ctx.author.id})
        
        fg = items.get(item)

        if fg is None:
            await ctx.send("Item not found")
            return

        price = fg[1] * amount
        name = fg[2]

        u_bal = bal["bank"]

        if u_bal < price:
            await ctx.send("You don't have enough money in your bank")
            return

        await self.update_bank(ctx.author.id, u_bal - price)

        for x in bag['bag']:
            if x[0] == item:
                init_amount = x[1]
                final_amount = amount + init_amount
                index = bag['bag'].index(x)
                await self.edit_item(ctx.author.id, index, final_amount)
                await ctx.send(f"You bought {amount} {name} for ${price}")
                return

        await self.add_item(ctx.author.id, item, amount)
        await ctx.send(f"You bought {amount} {name} for ${price}")   

    @commands.command(aliases=["s"])
    @cooldown(1, 2, BucketType.user)
    async def sell(self, ctx, item : str, amount : int = 1):
        """ Sell items from your bag """
        if amount <= 0 or amount > 100:
            await ctx.send("Amount must be greater than 0 or less than 0")
            return
        bal = await ecomoney.find_one({"id": ctx.author.id})
        if bal is None:
            await self.open_account(ctx.author.id)
            bal = await ecomoney.find_one({"id": ctx.author.id})

        bag = await ecobag.find_one({"id": ctx.author.id})
        if bag is None:
            await self.open_bag(ctx.author.id)
            bag = await ecobag.find_one({"id": ctx.author.id})
        
        fg = items.get(item)

        if fg is None:
            await ctx.send("Item not found")
            return

        price = fg[1]
        name = fg[2]

        u_bal = bal["bank"]

        for x in bag['bag']:
            if x[0] == item:
                init_amount = x[1]
                if amount > init_amount:
                    await ctx.send("You don't have enough of this item")
                    return
                elif amount == init_amount:
                    price = int(round(price * init_amount * 0.7,0))
                    index = bag['bag'].index(x)
                    await self.remove_item(ctx.author.id, item, init_amount)
                    await self.update_bank(ctx.author.id, u_bal + price)
                    await ctx.send(f"You sold {amount} {name} for ${price}")
                    return

                else:
                    final_amount = init_amount - amount
                    price =  int(round(price * amount * 0.7,0))
                    index = bag['bag'].index(x)
                    await self.edit_item(ctx.author.id, index, final_amount)
                    await self.update_bank(ctx.author.id, u_bal + price)
                    await ctx.send(f"You sold {amount} {name} for ${price}")
                    return

        await ctx.send("You don't have this item")

    @commands.command(aliases=["i"])
    @cooldown(1, 2, BucketType.user)
    async def inventory(self, ctx, page : int = 1):
        """ Checkout your inventory. For more than one page, use the page number.
        {1 : "0-9", 2 : "10-20", 3 : "20-30", 4 : "30-40", 5 : "40-50"} - Page and item number
        """
        if page > 5 or page < 1:
            await ctx.send("Page must be between 1 and 5")
            return
        bal = await ecomoney.find_one({"id": ctx.author.id})
        if bal is None:
            await self.open_account(ctx.author.id)
            bal = await ecomoney.find_one({"id": ctx.author.id})

        bag = await ecobag.find_one({"id": ctx.author.id})
        if bag is None:
            await self.open_bag(ctx.author.id)
            bag = await ecobag.find_one({"id": ctx.author.id})

        total = 0
        page_dict = {1 : "0-9", 2 : "10-20", 3 : "20-30", 4 : "30-40", 5 : "40-50"}
        intial, final = page_dict[page].split('-')
        for x in bag['bag']:
            total += 1
        if total == 0:
            await ctx.send("Your bag is empty")
            return
        
        page_items = bag['bag'][int(intial):int(final)+1]

        embed = discord.Embed(
            title=f"{ctx.author.name}'s Inventory",
            description=f"Page {page} | Total Items In Inventory: {total}",
            color=0xFF0000
            )
        for x in page_items:
            fg = items.get(x[0])
            embed.add_field(name=fg[2], value=f"{x[1]}", inline=False)

        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)

    # leaderboard
    @commands.command(aliases=["lb"])
    @cooldown(1, 2, BucketType.user)
    async def leaderboard(self, ctx):
        """ Checkout the leaderboard."""

        rankings = ecomoney.find().sort("bank", -1)

        i = 1

        embed = discord.Embed(
            title=f"{ctx.guild.name}'s Leaderboard",
            description=f"\u200b",
            color=0xFF0000
            )

        async for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tb = x["bank"]
                embed.add_field(
                    name=f"{i} : {temp.name}", value=f"Money: ${tb}", inline=False
                )
                i += 1
            except:
                pass
            if i == 11:
                break


        embed.set_footer(
            text=f"Requested By: {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}"
        )
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Shop(bot))
