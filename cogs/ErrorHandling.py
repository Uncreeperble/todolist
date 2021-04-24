import ast
import asyncio
import aiosqlite
import discord
import os
from discord.ext import commands
from modules import module
class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(':x: This command cannot be used in direct messages.')
            except discord.Forbidden:
                pass
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            msg = await ctx.send(":x: Only the bot owner may run this command")
            await asyncio.sleep(2)
            await msg.delete()
            await ctx.message.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title=":x: Missing Required Argument", description="This command required an argument to be given.", color=discord.Color.red())
            embed.set_footer(text=self.bot.footerText)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed=discord.Embed(title=":x: Bad Argument provided", description="The argument provided was not in the right form.", color=discord.Color.red())
            embed.set_footer(text=self.bot.footerText)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title=":x: Missing Permissions", description="To run this command you need the `manage guild` permission.", color=discord.Color.red())
            embed.set_footer(text=self.bot.footerText)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):
            embed=discord.Embed(title=":x: Command Invoke Error", description=f"{error}", color=discord.Color.red())
            embed.set_footer(text=self.bot.footerText)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(title=":x: Command Cooldown", description=f"{error}", color=discord.Color.red())
            embed.set_footer(text=self.bot.footerText)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(2)
            await msg.delete() 
            await ctx.message.delete()
        else:
            await ctx.send(f":x: There was an error. Contact Support with the error: `{error}`, link to support server: https://discord.gg/h5GKHEMaKd")


def setup(bot):
    bot.add_cog(ErrorHandling(bot))