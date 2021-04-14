import ast
import time
import asyncio
import discord
import random
import sqlite3
from discord.ext import commands
from discord.ext.commands import *
intents = discord.Intents.default()
conn = sqlite3.connect('bot.db')
c = conn.cursor()
default_prefix = 'b'
def get_prefix(bot, message):
    if checkIfSetup(message.guild.id):
        c.execute(f"SELECT prefix FROM config WHERE guildID = {message.guild.id}")
        return c.fetchone()[0]
    else:
        return default_prefix
def my_prefix(bot, message):
    return when_mentioned(bot, message) + [get_prefix(bot, message)]        
bot = commands.Bot(command_prefix=my_prefix,intents=intents, case_insensitive=True)
bot.remove_command("help")


footerText = "© 2021 Portal Development. All rights reserved - %support"

# <-------------------------- causal defs ------------------------------->


def checkIfSetup(guildID):
    c.execute(f"""
        SELECT *
        FROM config WHERE guildID = {guildID}
        """)
    config = c.fetchall()
    if str(config) != "[]":
        return True
    return False
    
async def updatePos(ctx):
    guildID = ctx.guild.id
    c.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
    amt = int(c.fetchone()[0])
    if amt != 0:
        c.execute(f"SELECT * FROM items WHERE guildID = {guildID} ORDER BY pos ASC")
        items = c.fetchall()
        c.execute(f"DELETE FROM items WHERE guildID = {guildID}")
        for i in range(amt):
            c.execute(f"""INSERT INTO items VALUES 
            ({ctx.guild.id}, "{items[i][1]}", {i+1})
        """)
            conn.commit()
    else:
        await ctx.send("nothing in list")
async def updateList(ctx, em, configInfo):
    channel = bot.get_channel(int(configInfo[4]))
    msg = await channel.fetch_message(int(configInfo[3]))
    await msg.delete()
    newMSG = await channel.send(embed=em)
    c.execute(f"""UPDATE config SET updatingMSG = {int(newMSG.id)} WHERE guildID = {ctx.guild.id}""")
    conn.commit()
def generateListEM(guildID):
    c.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
    upto = int(c.fetchone()[0])
    G = bot.get_guild(int(guildID))
    GNAME = G.name
    if upto != 0:
        c.execute(f"SELECT * FROM items WHERE guildID = {guildID} ORDER BY pos ASC")
        items = c.fetchall()
        SplitList = ""
        c.execute(f"SELECT listName from config WHERE guildID = {guildID}")
        lname = c.fetchone()[0]
        for i in range(upto):
            SplitList = SplitList + f"\n **{items[i][2]}:** {items[i][1]}"
        em = discord.Embed(title = f"{lname}", description ="", color = discord.Color.green())
        em.add_field(name=f"This server's list currently has {upto} item/s.", value=SplitList, inline=False)
        em.set_footer(text=footerText)
    else:
        em = discord.Embed(title = f"{GNAME}'s To-Do List", description ="", color = discord.Color.green())
        em.add_field(name=f"No items to be displayed.", value="`AddItem <Item>`", inline=False)
        em.set_footer(text=footerText)
    return em  
# <------------------------------------------------------------------------->


# <------------------------ BEFORE START UP EVENTS ---------------------------->
@bot.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)
    activity = discord.Game(name=f"Prefix % | {str(len(bot.guilds))} guilds", type=1)
    await bot.change_presence(status=discord.Status.online , activity=activity)

# <--------------------------------------------------------------------------->

# <--------------------------ERRORS------------------------------------->
@bot.event
async def on_command_error(ctx, error):
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
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed=discord.Embed(title=":x: Bad Argument provided", description="The argument provided was not in the right form.", color=discord.Color.red())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title=":x: Missing Permissions", description="To run this command you need the `manage guild` permission.", color=discord.Color.red())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        embed=discord.Embed(title=":x: Command Invoke Error", description=f"{error}", color=discord.Color.red())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed=discord.Embed(title=":x: Command Cooldown", description=f"{error}", color=discord.Color.red())
        embed.set_footer(text=footerText)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        await msg.delete() 
        await ctx.message.delete()
    else:
        await ctx.send(f":x: There was an error. Contact %support with the error: `{error}`")
# <--------------------------------------------------------------------------->


# <------------------------ Guild join & leave events ------------------------>
@bot.event
async def on_guild_join(guild):
    activity = discord.Game(name=f"Prefix % | {str(len(bot.guilds))} guilds", type=1)
    await bot.change_presence(status=discord.Status.online , activity=activity)
    em = discord.Embed(title="Bot Joined Server", description=f"""Guild Name: {str(guild.name)}, Guild ID: {str(guild.id)}
Bot Guild Count: {str(len(bot.guilds))}
""", color = discord.Color.green())
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
""", color = discord.Color.green())
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
@commands.is_owner()
async def eval_fn(ctx, *, cmd):
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
# <---------------------------------------------------------------------------------->    




# <------------------------------- simple text reply commands ---------------------------->  
@bot.command(aliases=['BetaTesting', 'Beta'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def BetaProgram(ctx):
    embed=discord.Embed(title="Beta Testers Program", description="""*Interested in becoming a beta tester?*
    --> To become a beta tester, [join the support server](https://discord.gg/pB77UUUxq3) and contact support.""", color=discord.Color.green())
    embed.set_footer(text=footerText)
    await ctx.send(embed=embed)    
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def help(ctx, page = 1):
    if page == 1:
        em = discord.Embed(title="ToDo-List Bot Help Menu (Pg. 1/3)", description="", color=discord.Color.green())
        em.add_field(name="The default prefix for the bot is `%`", value="""
        **Main Commands**
        `Setup` - Sets up the bot, creating all required roles and channels `(No aliases)`
        `Reset` - Resets the bot, deleting all roles and channels created `(No aliases)`
        `ViewList` - Displays the todo list `(Aliases: View, View_List, List, Items)`
        `AddItem <item>` - Adds an item to the list `(Aliases: Add, Add_Item)`
        `EditItem <itemID> <New item>` - Edits an item `(Aliases: Edit, Edit_Item)`
        `DeleteItem <itemID>` - Deletes an item `(Aliases: DelItem, Delete_Item, Del)`
        `ClearList` - Clears the current list `(Aliases: Clear, Clear_List)`
        `Done <itemID>` - Marks an item as completed `(Aliases: Finish, Complete)`
        """, inline=True)
        em.set_footer(text="© 2021 Portal Development. All rights reserved - `%help 2` for more")
    elif page == 2:
        em = discord.Embed(title="ToDo-List Bot Help Menu (Pg. 2/3)", description="", color=discord.Color.green())
        em.add_field(name="The default prefix for the bot is `%`", value="""
        **Other commands**
        `Help <page>` - Displays all of the bot commands `(No aliases)`
        `Ping` - Displays the latency of the bot `(No aliases)`
        `Invite` - Displays the invite link of the bot `(No aliases)`
        `About` - Displays the bot information and invite link `(No aliases)`
        `Support` - Displays a link to the support server `(No aliases)`
        `Info` - Displays credits of the bot `(Aliases: Credits, Author)`
        `BetaProgram` - Displays all of the bot commands `(Aliases: BetaTesting, Beta)`
        `Stats` - Displays statistics of the bot `(Aliases: Statistics, GuildCount)`
        `ReportBug <Info>` - Reports a bug `(Aliases: Report_Bug, BugReport)`
        `Suggestion <Info>` - Makes a suggestion `(Aliases: Suggest, MakeSuggestion)`               
        """, inline=True)
        em.set_footer(text="© 2021 Portal Development. All rights reserved - `%help 1` for first page")
    elif page == 3:
        em = discord.Embed(title="ToDo-List Bot Help Menu (Pg. 3/3)", description="", color=discord.Color.green())
        em.add_field(name="The default prefix for the bot is `%`", value="""
        **Config commands**
        `Prefix <prefix>` - Changes the guilds prefix `(Aliases: SetPrefix)`
        `EnableChecking` - Allows the use of the Done command `(No aliases)`
        `SetListName <New List Name>` - Changes the list name `(No aliases)`
        """, inline=True)
        em.set_footer(text="© 2021 Portal Development. All rights reserved - `%help 1` for first page")
    else:
        await ctx.send("Incorrect page number.")
    await ctx.send(embed=em)
#################################    
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def ping(ctx):
    await ctx.send("Bot latency is `" + str(round(bot.latency * 1000)) + "ms`")
##################################
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def invite(ctx):
    embed=discord.Embed(title="Click me to invite the Bot", url="https://top.gg/bot/782105629572464652/invite/", description="The link provided gives the bot Administrator permissions.", color=discord.Color.green())
    embed.set_footer(text=footerText)
    await ctx.send(embed=embed)
##########################################
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def about(ctx):    
    em = discord.Embed(title="About To-Do List Bot", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/) for more information about the bot.
    
    You can invite the bot by clicking [here](https://discord.com/oauth2/authorize?client_id=782105629572464652&scope=bot&permissions=8)
""", color = discord.Color.green())
    em.set_footer(text=footerText)
    await ctx.send(embed=em)
#################################################
@bot.command(aliases=['credits', 'author'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def info(ctx):
    em = discord.Embed(title="To-Do List Bot", description=f"""Please visit our [site](https://todolistbot.zyrosite.com/) for more information about the bot.
Stats:
Server Count: {str(len(bot.guilds))} servers
Director: Thomas Morton
Developer: Benjamin - E (Uncreeperble#2072)
Framework: Python""", color=discord.Color.green())
    em.set_footer(text=footerText)
    await ctx.send(embed=em)
##################################################
@bot.command(aliases=['statistics','guildcount'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def stats(ctx):
    embed=discord.Embed(title="Bot statistics", description=f"""Guild Count: `{str(len(bot.guilds))}`
Member Count: `{str(sum(g.member_count for g in bot.guilds))}`
    """, color=discord.Color.green())
    embed.set_footer(text=footerText)
    await ctx.send(embed=embed)
###################################################
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def support(ctx):
    await ctx.send("For bot support or to contact the developer join this server: https://discord.gg/pB77UUUxq3")
# <---------------------------------------------------------------------------------->    

# <.---------------------------- suggest and report -------------------------------->
@bot.command(aliases=['Suggest', 'MakeSuggestion'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def Suggestion(ctx, *, Suggestion):
    channel = bot.get_channel(812601965850263602)
    em = discord.Embed(title=f"New Suggestion from {ctx.guild.name}", description=f"""`{Suggestion}`
        
        Guild ID: `{ctx.guild.id}`
        User ID: `{ctx.author.id}`
        Username: `{ctx.author.name}{ctx.author.discriminator}`
        """, color=discord.Color.green())
    em.set_footer(text=footerText)
    await channel.send(embed=em)  
    em = discord.Embed(title=f"Suggestion Sent To Developers", description=f"""Developer Recieved:
    
        `{Suggestion}`
        
        Guild ID: `{ctx.guild.id}`
        User ID: `{ctx.author.id}`
        Username: `{ctx.author.name}#{ctx.author.discriminator}`
        """, color=discord.Color.green())
    em.set_footer(text=footerText)
    await ctx.send(embed=em)    
################################################################################
@bot.command(aliases=['Report_Bug', 'BugReport'])
@commands.cooldown(1, 3, commands.BucketType.guild)
async def ReportBug(ctx, *, Bug):
    channel = bot.get_channel(812601965850263602)
    em = discord.Embed(title=f"New Bug Report from {ctx.guild.name}", description=f"""`{Bug}`
        
        Guild ID: `{ctx.guild.id}`
        User ID: `{ctx.author.id}`
        Username: `{ctx.author.name}#{ctx.author.discriminator}`
        """, color=discord.Color.green())
    em.set_footer(text=footerText)
    await channel.send(embed=em)  
    em = discord.Embed(title=f"Bug Report Sent To Developers", description=f"""Developer Recieved:
    
        `{Bug}`
        
        Guild ID: `{ctx.guild.id}`
        User ID: `{ctx.author.id}`
        Username: `{ctx.author.name}#{ctx.author.discriminator}`
        """, color=discord.Color.green())
    em.set_footer(text=footerText)
    await ctx.send(embed=em)  
# <----------------------------------------------------------------------->


# <-------------------------------    Setup and Reset command    ---------------------------->    
@bot.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def setup(ctx):
    if ctx.guild.me.guild_permissions.manage_roles == False or ctx.guild.me.guild_permissions.manage_channels == False:
        embed = discord.Embed(title="Bot missing Permissions", description="To Run this command the bot needs the `Manage Roles` and `Manage Channels` permissions.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
    else:
        if checkIfSetup(ctx.guild.id):  
            embed=discord.Embed(title="This server has already been setup yet.", description="Please run the reset command if you wish to re-run the setup.", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
        else:   
            errors = []
            startTime = time.time()
            try:
                role1 = await ctx.guild.create_role(name="View List")
                errors.append(f":white_check_mark: Created View List role")
            except:
                errors.append(":x: Failed to create the View List role")  
            try:
                role2 = await ctx.guild.create_role(name="List Management")
                errors.append(f":white_check_mark: Created List Management role")
                
            except:
                errors.append(":x: Failed to create the List Management role")
            server = ctx.guild
            role = discord.utils.get(server.roles,name="View List")
            overwrites = {
            server.default_role: discord.PermissionOverwrite(read_messages=False),
            server.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
                }
            try:
                listChannel = await server.create_text_channel('todo-list',overwrites=overwrites)
                list = []
                embed = discord.Embed(title= f"{ctx.guild.name}'s To-Do List", description="To add items please type %additem <item name>",color=discord.Color.green())
                updating_list = await listChannel.send(embed=embed)
                
                errors.append(f":white_check_mark: Created the <#{listChannel.id}> channel")
            except:
                errors.append(":x: Failed to create the todo-list channel") 
            try:
                c.execute(f"""INSERT INTO config
                
            VALUES
            (
            {role1.id}, {role2.id}, {ctx.guild.id}, {updating_list.id}, {listChannel.id}, 'b', '{ctx.guild.name}s ToDo List'
            )
            """)
                conn.commit()
                errors.append(":white_check_mark: Updated the guild config database")
            except:
                errors.append(":x: Failed to update the guild config database")
            test = '\n'.join(errors)
            em = discord.Embed(title="Setup Complete", description=f"The Setup was completed in {round(time.time() - startTime, 4)} seconds.", color=discord.Color.green())
            em.add_field(name="The following has been changed:", value=test)
            em.set_footer(text=footerText)
            await ctx.send(embed=em)    

#########################################################
@bot.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def reset(ctx):
    embed = discord.Embed(title=f"Please Confirm", description="Please react with :white_check_mark: to perform a full reset.", color=discord.Color.green())
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
        embed = discord.Embed(title="TimeOut Error", description="You did not react in time, reset cancelled.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        NotTimeout = False
        await ctx.send(embed=embed)
    if NotTimeout:
        if str(reaction.emoji) == "\U0000274e":
            embed = discord.Embed(title="Reset Cancelled", description="The reset was cancelled, no changes were made.", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
        else:
            errors = []
            if checkIfSetup(ctx.guild.id):  
                ServerSetup = True
                c.execute(f"SELECT * FROM config WHERE guildID = {ctx.guild.id}")
                try:
                    configInfo = list(c.fetchone())
                except:
                    errors.append(":x: Could not fetch config info")
                    configInfo = [1,2,3,4,5]
           
            else:
                ServerSetup = False
            if ServerSetup:
                startTime = time.time()
                channel = bot.get_channel(int(configInfo[4]))
                role = ctx.guild.get_role(int(configInfo[0]))
                role2 = ctx.guild.get_role(int(configInfo[1]))

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
                    c.execute(f"DELETE FROM config WHERE guildID = {ctx.guild.id}")
                    conn.commit()
                    errors.append(":white_check_mark: Guild Config database deleted")
                except:
                    errors.append(":x: Failed to delete the guild config-info database")
                try:
                    c.execute(f"DELETE FROM items WHERE guildID = {ctx.guild.id}")
                    conn.commit()
                    errors.append(":white_check_mark: List Items database deleted")
                except:
                    errors.append(":x: Failed to delete the guild list-items database")
                test = '\n'.join(errors)
                em = discord.Embed(title="Reset Complete", description=f"The Reset was completed in {round(time.time() - startTime, 4)} seconds.", color=discord.Color.green())
                em.add_field(name="The following has been changed:", value=test)
                em.set_footer(text=footerText)
                await ctx.send(embed=em)                    
                
            else:
                embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
                embed.set_footer(text=footerText)
                await ctx.send(embed=embed)
    else:
        return

    

# <---------------------------------------------------------------------------------->    


# <-------------------------------    List manage and view commands    ---------------------------->   
@bot.command(aliases=['view','view_list','list','items'])
@commands.guild_only()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def viewlist(ctx, guildID=None):
    if str(ctx.author.id) == "527990415786508299":
        if guildID == None:
            guildID = ctx.guild.id
    else:
        guildID = ctx.guild.id
    if checkIfSetup(ctx.guild.id):  
        ServerSetup = True
        c.execute(f"SELECT * FROM config WHERE guildID = {ctx.guild.id}")
        configInfo = list(c.fetchall()[0])

        role = ctx.guild.get_role(int(configInfo[0]))
    else:
        ServerSetup = False
    if ServerSetup:
        if role in ctx.author.roles or guildID != ctx.guild.id:
            em = generateListEM(guildID)
            await ctx.send(embed=em)
        else:
            embed=discord.Embed(title=":x: No Permission.", description="You require the `View List` role to run this command!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
#############################################################################
@bot.command(aliases=['add','add_item'])
@commands.guild_only()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def additem(ctx, *, defInput):
    guildID = ctx.guild.id
    if checkIfSetup(ctx.guild.id):  
           ServerSetup = True
           c.execute(f"SELECT * FROM config WHERE guildID = {guildID}")
           configInfo = list(c.fetchall()[0])
           role = ctx.guild.get_role(int(configInfo[1]))
    else:
        ServerSetup = False
    if ServerSetup:
        if role in ctx.author.roles or guildID != ctx.guild.id:

            c.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {ctx.guild.id}")
            upto = int(c.fetchone()[0]) + 1
            c.execute(f"""INSERT INTO items VALUES (
            {ctx.guild.id}, '{defInput}', {upto}
            )""")
            conn.commit()
            em = generateListEM(ctx.guild.id)
            await updateList(ctx, em, configInfo)
            em = discord.Embed(title = f":white_check_mark: Item added", description =f"`{defInput}` was added to the todo list in position {upto}", color = discord.Color.green())
            em.set_footer(text=footerText)
            await ctx.send(embed=em)

        else:
            embed=discord.Embed(title=":x: No Permission.", description="You require the `List Management` role to run this command!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
#####################################################################################
@bot.command(aliases=['clear_list', 'clear'])
@commands.guild_only()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def clearlist(ctx):
    guildID = ctx.guild.id
    if checkIfSetup(ctx.guild.id):  
       ServerSetup = True
       c.execute(f"SELECT * FROM config WHERE guildID = {guildID}")
       configInfo = list(c.fetchone())
       role = ctx.guild.get_role(int(configInfo[1]))
    else:
        ServerSetup = False
    if ServerSetup:
        if role in ctx.author.roles or guildID != ctx.guild.id:
            embed=discord.Embed(title="Please Confirm", description="Please react with :white_check_mark: to clear the list.", color=discord.Color.green())
            message = await ctx.send(embed=embed)
            await message.add_reaction("\U00002705")
            await message.add_reaction("\U0000274e")
            Nottimeout = True
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["\U00002705", "\U0000274e"]
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)
            except:
                embed=discord.Embed(title="TimeOut Error", description="You did not react in time, action cancelled.", color=discord.Color.green())
                embed.set_footer(text=footerText)
                await ctx.send(embed=embed)
                Nottimeout = False
            if Nottimeout:
                if str(reaction.emoji) == "\U0000274e":
                    embed=discord.Embed(title="Action Cancelled", description="The list has not been cleared due to cancellation.", color=discord.Color.green())
                    embed.set_footer(text=footerText)
                    await ctx.send(embed=embed)
                elif str(reaction.emoji) == "\U00002705":
                    c.execute(f"DELETE FROM items WHERE guildID = {guildID}")
                    conn.commit()
                    em = generateListEM(guildID)
                    await updateList(ctx, em, configInfo)
                    embed=discord.Embed(title="List Cleared", description="The list has been cleared.", color=discord.Color.green())
                    embed.set_footer(text=footerText)
                    await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=":x: No Permission.", description="You require the `List Management` role to run this command!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
########################################################################################################
@bot.command(aliases=['delitem', 'del', 'delete_item'])
@commands.guild_only()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def deleteItem(ctx, defInput : int):
    guildID = ctx.guild.id
    if checkIfSetup(ctx.guild.id):  
       ServerSetup = True
       c.execute(f"SELECT * FROM config WHERE guildID = {guildID}")
       configInfo = list(c.fetchall()[0])
       role = ctx.guild.get_role(int(configInfo[1]))
       c.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
       upto = c.fetchone()[0]

    else:
        ServerSetup = False
    if ServerSetup:
        if role in ctx.author.roles or guildID != ctx.guild.id:
            if int(defInput) <= int(upto) and int(defInput) > 0:
                c.execute(f"DELETE FROM items WHERE pos = {defInput} AND guildID = {ctx.guild.id}")
                conn.commit()
                await updatePos(ctx)
                em = generateListEM(ctx.guild.id)
                await updateList(ctx, em, configInfo)
                embed=discord.Embed(title="Item Deleted", description=f"The item in position `{defInput}` was deleted.", color=discord.Color.green())
                embed.set_footer(text=footerText)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Invalid ID.", description="The id provided was not valid.", color=discord.Color.green())
                embed.set_footer(text=footerText)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=":x: No Permission.", description="You require the `List Management` role to run this command!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)    
# <----------------------------------------------------------------------------------------------->  

@bot.command(aliases=['edit', 'edit_item'])
@commands.guild_only()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def editItem(ctx, defInput : int, *, newItem):
    guildID = ctx.guild.id
    if checkIfSetup(ctx.guild.id):  
       ServerSetup = True
       c.execute(f"SELECT * FROM config WHERE guildID = {guildID}")
       configInfo = list(c.fetchall()[0])
       role = ctx.guild.get_role(int(configInfo[1]))
       c.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
       upto = c.fetchone()[0]

    else:
        ServerSetup = False
    if ServerSetup:
        if role in ctx.author.roles or guildID != ctx.guild.id:
            if int(defInput) <= int(upto) and int(defInput) > 0:
                c.execute(f"""UPDATE items SET item = '{str(newItem)}' WHERE pos = {int(defInput)} AND guildID = {ctx.guild.id}""")
                conn.commit()
                em = generateListEM(ctx.guild.id)
                await updateList(ctx, em, configInfo)
                embed=discord.Embed(title="Item Edited", description=f"The item in position `{defInput}` was edited to `{newItem}`.", color=discord.Color.green())
                embed.set_footer(text=footerText)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Invalid ID.", description="The id provided was not valid.", color=discord.Color.green())
                embed.set_footer(text=footerText)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=":x: No Permission.", description="You require the `List Management` role to run this command!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
        

@bot.command(aliases=['SetPrefix'])
@commands.guild_only()
@commands.has_guild_permissions(manage_guild=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def prefix(ctx, prefix = None):
    if prefix is not None:
        if len(prefix) <= 3:
            c.execute(f"""UPDATE config WHERE guildID = {ctx.guild.id} SET prefix = '{str(prefix)}'""")
            conn.commit()
            embed=discord.Embed(title="Prefix Updated", description=f"Your server prefix has been changed to `{prefix}`", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=":x: Too Long", description="The server prefix can only be up to 3 characters long!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        if checkIfSetup(ctx.guild.id):
            c.execute(f"SELECT prefix FROM config WHERE guildID = {ctx.guild.id}")
            pf = c.fetchone()[0]
        else:
            pf = default_prefix
        embed=discord.Embed(title="Server Prefix", description=f"The server prefix is currently: `{pf}`", color=discord.Color.green())
        embed.set_footer(text=footerText)
        await ctx.send(embed=embed)
        
        
@bot.command()
@commands.guild_only()
@commands.cooldown(1, 5, commands.BucketType.guild)
async def SetListName(ctx, *, newName):
    guildID = ctx.guild.id
    if checkIfSetup(ctx.guild.id):  
       ServerSetup = True
       c.execute(f"SELECT * FROM config WHERE guildID = {guildID}")
       configInfo = list(c.fetchall()[0])
       role = ctx.guild.get_role(int(configInfo[1]))
       c.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
       upto = c.fetchone()[0]

    else:
        ServerSetup = False
    if ServerSetup:
        if role in ctx.author.roles or guildID != ctx.guild.id:
            c.execute(f"""UPDATE config SET listName = '{str(newName)}' WHERE guildID = {ctx.guild.id} """)
            conn.commit()
            em = generateListEM(ctx.guild.id)
            await updateList(ctx, em, configInfo)
            embed=discord.Embed(title="List Name Updated", description=f"Your server list name has been changed to `{newName}`", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=":x: No Permission.", description="You require the `List Management` role to run this command!", color=discord.Color.green())
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
        embed.set_footer(text=footerText)   
    # <-----------------------------------------Bot login ----------------------------------->
bot.run("Nzk4NzQ0MjYzOTU2ODg5NjAx.X_5ekA.5h94UI5FkZaouUJFtJKdmaKOYZg") 
# latest update 2.1.5
