import ast
import time
import discord
import random
import sqlite3
from discord.ext import commands
from discord.ext.commands import *
intents = discord.Intents.default()
conn = sqlite3.connect('bot.db')
bot = commands.Bot(command_prefix=when_mentioned_or('b'),intents=intents)
c = conn.cursor()
@bot.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)
@bot.event
async def on_guild_join(guild):
    activity = discord.Game(name=f"Prefix % | {str(len(bot.guilds))} guilds", type=1)
    await bot.change_presence(status=discord.Status.online , activity=activity)
    em = discord.Embed(title="Bot Joined Server", description=f"""Guild Name: {str(guild.name)}, Guild ID: {str(guild.id)}
Bot Guild Count: {str(len(bot.guilds))}

""", color = 0x00a8ff)
    em.set_footer(text=footerText)
    channel = bot.get_channel(812605561643466762)
    await channel.send(embed=em)
@bot.event
async def on_guild_remove(guild):
    activity = discord.Game(name=f"Prefix % | {str(len(bot.guilds))} guilds", type=1)
    await bot.change_presence(status=discord.Status.online , activity=activity)
    em = discord.Embed(title="Bot Left Server", description=f"""Guild Name: {str(guild.name)}, Guild ID: {str(guild.id)}
Bot Guild Count: {str(len(bot.guilds))}

""", color = 0x00a8ff)
    em.set_footer(text=footerText)
    channel = bot.get_channel(812605561643466762)
    await channel.send(embed=em)    
def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
@bot.command()
async def eval_fn(ctx, *, cmd):
    print(f"{ctx.author.name} ran the command eval_fn")
    if str(ctx.author.id) == "527990415786508299":
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)
        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)
    else:
        await ctx.send(":warnign: You will be blacklisted if you continue to try and run DEVELOPER ONLY commands")
           

bot.run("Nzk4NzQ0MjYzOTU2ODg5NjAx.X_5ekA.5h94UI5FkZaouUJFtJKdmaKOYZg") 
