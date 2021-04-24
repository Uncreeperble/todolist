import ast
import asyncio
import aiosqlite
import discord
import os
from discord.ext import commands
from modules import module

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Displays the latency of the bot.")
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def ping(self, ctx):
        await ctx.send("Bot latency is `" + str(round(self.bot.latency * 1000)) + "ms`")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def about(self, ctx):    
        em = discord.Embed(title="About To-Do List Bot", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/) for more information about the bot.
        
        You can invite the bot by clicking [here](https://discord.com/oauth2/authorize?client_id=782105629572464652&scope=bot&permissions=8)
    """, color = discord.Color.green())
        em.set_footer(text=self.bot.footerText)
        await ctx.send(embed=em)
    
    @commands.command(aliases=['credits', 'author'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def info(self, ctx):
        em = discord.Embed(title="To-Do List Bot", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/) for more information about the bot.

    Stats:
    Server Count: {str(len(self.bot.guilds))} servers

    Director: Thomas Morton
    Developer: Benjamin - E (Uncreeperble#2072)
    Framework: Python""", color=discord.Color.green())
        em.set_footer(text=self.bot.footerText)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def invite(self, ctx):
        embed=discord.Embed(title="Click me to invite the Bot", url="https://top.gg/bot/782105629572464652/invite/", description="The link provided gives the bot Administrator permissions.", color=discord.Color.green())
        embed.set_footer(text=self.bot.footerText)
        await ctx.send(embed=embed)

    @commands.command(aliases=['statistics','guildcount'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def stats(self, ctx):
        embed=discord.Embed(title="Bot statistics", description=f"""
        Guild Count: `{str(len(self.bot.guilds))}`
        Member Count: `{str(sum(g.member_count for g in self.bot.guilds))}`

        """, color=discord.Color.green())
        embed.set_footer(text=self.bot.footerText)
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['BetaTesting', 'Beta'])
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def BetaProgram(self, ctx):
        embed=discord.Embed(title="Beta Testers Program", description="""*Interested in becoming a beta tester?*
        
        --> To become a beta tester, [join the support server](https://discord.gg/pB77UUUxq3) and contact support.""", color=discord.Color.green())
        embed.set_footer(text=self.bot.footerText)
        await ctx.send(embed=embed)   


    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def Support(self, ctx):
        embed=discord.Embed(title="ToDo List Bot", description="""Please visit our [site](https://todolistbot.zyrosite.com/) for more information
        
        Please [join the support server](https://discord.gg/pB77UUUxq3) if you need further support.""", color=discord.Color.green())
        embed.set_footer(text=self.bot.footerText)
        await ctx.send(embed=embed)   
def setup(bot):
    bot.add_cog(Other(bot))