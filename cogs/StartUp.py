import ast
import asyncio
import aiosqlite
import discord
import os
from discord.ext import commands
from modules import module
class StartUp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot running with:")
        print("Username: ", self.bot.user.name)
        print("User ID: ", self.bot.user.id)
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        activity = discord.Game(name=f"Prefix % | {str(len(bot.guilds))} guilds", type=1)
        await bot.change_presence(status=discord.Status.online , activity=activity)
        em = discord.Embed(title="Bot Joined Server", description=f"""Guild Name: {str(guild.name)}, Guild ID: {str(guild.id)}
    Bot Guild Count: {str(len(bot.guilds))}
    """, color = discord.Color.green())
        em.set_footer(text=ctx.bot.footerText)
        channel = bot.get_channel(812605561643466762)
        await channel.send(embed=em)
    ############################################
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        activity = discord.Game(name=f"Prefix % | {str(len(bot.guilds))} guilds", type=1)
        await bot.change_presence(status=discord.Status.online , activity=activity)
        em = discord.Embed(title="Bot Left Server", description=f"""Guild Name: {str(guild.name)}, Guild ID: {str(guild.id)}
    Bot Guild Count: {str(len(bot.guilds))}
    """, color = discord.Color.green())
        em.set_footer(text=ctx.bot.footerText)
        channel = bot.get_channel(812605561643466762)
        await channel.send(embed=em)  


def setup(bot):
    bot.add_cog(StartUp(bot))