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

# <-------------------------- causal defs ------------------------------->
def checkTableExists(tablename):
    try:
        c.execute(f"""
            SELECT *
            FROM {tablename}
            """)
        return True
    except:
        return True

# <------------------------------------------------------------------------->


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
    em.add_field(name="Commands", value="""=-=-=-=-=-=-=-=-=-=-=-=-=
    **Main Commands**
    `Setup` - Sets up the bot, creating all required roles and channels `(No aliases)`
    `Reset` - Resets the bot, deleting all roles and channels created `(No aliases)`
    =-=-=-=-=-=-=-=-=-=-=-=-=
    **Other commands**
    `Help` - Displays all of the bot commands `(No aliases)`
    `Ping` - Displays the latency of the bot `(No aliases)`
    `Invite` - Displays the invite link of the bot `(No aliases)`
    `About` - Displays the bot information and invite link `(No aliases)`
    `Stats` - Displays statistics of the bot `(Aliases: Statistics, GuildCount)`
    `Info` - Displays credits of the bot `(Aliases: Credits, Author)`
    =-=-=-=-=-=-=-=-=-=-=-=-=""", inline=True)
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
    embed.set_footer(text=footerText)
    await ctx.send(embed=embed)
##########################################
@bot.command()
async def about(ctx):    
    em = discord.Embed(title="About To-Do List Bot", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/) for more information about the bot.
    
    You can invite the bot by clicking [here](https://discord.com/oauth2/authorize?client_id=782105629572464652&scope=bot&permissions=8)
""", color = 0x00a8ff)
    em.set_footer(text=footerText)
    await ctx.send(embed=em)
#################################################
@bot.command(aliases=['credits', 'author'])
async def info(ctx):
    em = discord.Embed(title="To-Do List Bot", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/) for more information about the bot.

Stats:
Server Count: {str(len(bot.guilds))} servers

Director: Thomas Morton
Developer: Benjamin - E (Uncreeperble#2072)
Framework: Python""", color=0x00a8ff)
    em.set_footer(text=footerText)
    await ctx.send(embed=em)
##################################################
@bot.command(aliases=['statistics','guildcount'])
async def stats(ctx):
    embed=discord.Embed(title="Bot statistics", description=f"""Guild Count: `{str(len(bot.guilds))}`

Member Count: `{str(sum(g.member_count for g in bot.guilds))}`
    """, color=0x00a8ff)
    embed.set_footer(text=footerText)
    await ctx.send(embed=embed)
###################################################
# <---------------------------------------------------------------------------------->    




# <-------------------------------    Setup and Reset command    ---------------------------->    
@bot.command()
async def setup(ctx):
    await ctx.send("WHY")
#########################################################
@bot.command()
async def reset(ctx):
    if ctx.author.guild_permissions.manage_guild:
        if ctx.guild.me.guild_permissions.manage_roles == False or ctx.guild.me.guild_permissions.manage_channels == False:
            embed = discord.Embed(title="Bot missing Permissions", description="To Run this command the bot needs the `Manage Roles` and `Manage Channels` permissions.", color=0x00a8ff)
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Please Confirm", description="Please react with :white_check_mark: to perform a full reset.", color=0x00a8ff)
            embed.set_footer(text=footerText)
            message =  await ctx.send(embed=embed)
            await message.add_reaction("\U00002705")
            await message.add_reaction("\U0000274e")
            NotTimeout = True
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["\U00002705", "\U0000274e"]
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
            except:
                embed = discord.Embed(title="TimeOut Error", description="You did not react in time, reset cancelled.", color=0x00a8ff)
                embed.set_footer(text=footerText)
                NotTimeout = False
                await ctx.send(embed=embed)
            if NotTimeout:
                if str(reaction.emoji) == "\U0000274e":
                    embed = discord.Embed(title="Reset Cancelled", description="The reset was cancelled, no changes were made.", color=0x00a8ff)
                    embed.set_footer(text=footerText)
                    await ctx.send(embed=embed)
                else:
                    
                    if checkTableExists(f"config{ctx.guild.id}"):  
                        ServerSetup = True
                        # c.execute(f"SELECT * FROM config{ctx.guild.id}")
                        # configInfo = c.fetchall()[0]
                        configInfo = (823521117415276554, 823521118530699285, 721784188189016226, 823521234175262751, 823521119956107274)
                    else:
                        ServerSetup = False
                    if ServerSetup:
                        channel = ctx.guild.get_channel(int(configInfo[4]))
                        role = ctx.guild.get_role(int(configInfo[0]))
                        role2 = ctx.guild.get_role(int(configInfo[1]))
                        errors = []
                        try:
                            await channel.delete()
                            errors.append(":white_check_mark: ToDo List Channel was deleted")
                        except:
                            errors.append(":x: Failed to delete the todo list channel")
                        try:
                            await role.delete()
                            errors.append(":white_check_mark: View List Role was deleted")
                        except:
                            errors.append(":x: Failed to delete the View List role")
                        try:
                            await role2.delete()
                            errors.append(":white_check_mark: List Management Role was deleted")
                        except:
                            errors.append(":x: Failed to delete the List management role")
                        try:
                            c.execute(f"DROP TABLE config{ctx.guild.id}")
                            errors.append(":white_check_mark: Guild Config database deleted")
                        except:
                            errors.append(":x: Failed to delete the guild config-info database")
                        try:
                            c.execute(f"DROP TABLE items{ctx.guild.id}")
                            errors.append(":white_check_mark: List Items database deleted")
                        except:
                            errors.append(":x: Failed to delete the guild list-items database")
                        print(errors)
                        if errors == [":white_check_mark: ToDo List Channel was deleted", ":white_check_mark: View List Role was deleted", ":white_check_mark: List Management Role was deleted", ":white_check_mark: Guild Config database deleted", ":white_check_mark: List Items database deleted"]:
                            em = discord.Embed(title="Reset Complete", description="The Reset has been successful.", color=0x00a8ff)
                            em.add_field(name="The following has been changed:", value=""":white_check_mark: ToDo List Channel was deleted
                            :white_check_mark: View List Role was deleted
                            :white_check_mark: List Management Role was deleted
                            :white_check_mark: Guild Config database deleted
                            :white_check_mark: List Items database deleted
                            """)
                            em.set_footer(text=footerText)
                            await ctx.send(embed=em)
                        else:
                            test = '\n'.join(errors)
                            em = discord.Embed(title="Reset Complete", description="The Reset was not fully successful.", color=0x00a8ff)
                            em.add_field(name="The following has been changed:", value=test)
                            em.set_footer(text=footerText)
                            await ctx.send(embed=em)                    
                        
                    else:
                        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=0x00a8ff)
                        embed.set_footer(text=footerText)
                        await ctx.send(embed=embed)
            else:
                return
    else:
        embed=discord.Embed(title=":x: No Permissions.", description="You require the `manage guild` permission to run this command!", color=0x00a8ff)
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
    

# <---------------------------------------------------------------------------------->    



# <-----------------------------------------Bot login ----------------------------------->
bot.run("Nzk4NzQ0MjYzOTU2ODg5NjAx.X_5ekA.5h94UI5FkZaouUJFtJKdmaKOYZg") 
