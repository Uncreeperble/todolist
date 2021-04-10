import ast
import time
import discord
import random
import sqlite3
from discord.ext import commands
from discord.ext.commands import *
intents = discord.Intents.default()
conn = sqlite3.connect('bot.db')
bot = commands.Bot(command_prefix=when_mentioned_or('b'),intents=intents, case_insensitive=True)
bot.remove_command("help")
c = conn.cursor()

footerText = "© 2021 Portal Development. All rights reserved - %support"


# <------------------------ BEFORE START UP EVENTS ---------------------------->
@bot.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

# <--------------------------------------------------------------------------->




# <------------------------ Guild join & leave events ------------------------>
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
############################################
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
# <--------------------------------------------------------------------------->

    
    
    
# <----------------------------------------- eval command ------------------------>
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
        await ctx.send(":warning: You will be blacklisted if you continue to try and run DEVELOPER ONLY commands")
# <---------------------------------------------------------------------------------->    




# <------------------------------- simple text reply commands ---------------------------->       
@bot.command()
async def help(ctx):
    em = discord.Embed(title="ToDo-List Bot Help Menu", description="The default prefix for the bot is `%`", color=0x00a8ff)
    em.add_field(name="Commands", value="""
    `Help` - Displays all of the bot commands `(No aliases)`
    `Ping` - Displays the latency of the bot `(No aliases)`
    `Invite` - Displays the invite link of the bot `(No aliases)`
    `About` - Displays the bot information and invite link `(Aliases: Info, Credits)`
    `Stats` - Displays statistics of the bot `(Aliases: statistics, guildcount)`""", inline=True)
    em.set_footer(text=footerText)
    await ctx.send(embed=em)
#################################    
@bot.command()
async def ping(ctx):
    await ctx.send("Bot latency is `" + str(round(bot.latency * 1000)) + "ms`")
##################################
@bot.command()
async def invite(ctx):
    embed=discord.Embed(title="Click me to invite the Bot", url="https://top.gg/bot/782105629572464652/invite/", description="The link provided gives the bot Administrator permissions.", color=0x00a8ff)
    await ctx.send(embed=embed)
##########################################
@bot.command(aliases=['info', 'credits'])
async def about(ctx):    
    em = discord.Embed(title="To-Do List Bot Credits", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/)
""", color = 0x00a8ff)
    em.set_footer(text=footerText)
    await ctx.send(embed=em)
##################################################
@bot.command(aliases=['statistics','guildcount'])
async def stats(ctx):
    embed=discord.Embed(title="Bot statistics", description=f"""Guild Count: `{str(len(bot.guilds))}`
    
Member Count: `{str(sum(g.member_count for g in bot.guilds))}`
    """, color=0x00a8ff)
    await ctx.send(embed=embed)
###################################################

# <-----------------------------------------Bot login ----------------------------------->
bot.run("Nzk4NzQ0MjYzOTU2ODg5NjAx.X_5ekA.5h94UI5FkZaouUJFtJKdmaKOYZg") 
