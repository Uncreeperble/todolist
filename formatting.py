import ast
import asyncio
import aiosqlite
import discord
import os
from discord.ext import commands
intents = discord.Intents.default()

default_prefix = 'b'
async def get_prefix(bot, message):
    try:
        return await bot.db.execute("SELECT prefix FROM config WHERE guildID = ?", (message.guild.id))
    except:
        return default_prefix
async def my_prefix(bot, message):
    return commands.when_mentioned(bot, message) + [await get_prefix(bot, message)]        
bot = commands.Bot(command_prefix=my_prefix,intents=intents, case_insensitive=True, activity = discord.Game(name=f"Prefix % | Working On Updates", type=1) , status = discord.Status.online, help_command=None)


bot.db = bot.loop.run_until_complete(aiosqlite.connect("bot.db"))
bot.footerText = "© 2021 Portal Development. All rights reserved - %support"
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.guild)
async def help(ctx, page = 1):
    if page == 1 or page != 2 or page != 3:
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
        `Done <itemID>` - Marks an item as completed (If enabled)`(Aliases: Finish, Complete)`
        """, inline=True)
        em.set_footer(text="© 2021 Portal Development. All rights reserved - `help <1 | 2 | 3>` for help")
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
        em.set_footer(text="© 2021 Portal Development. All rights reserved - `help <1 | 2 | 3>` for help")
    elif page == 3:
        em = discord.Embed(title="ToDo-List Bot Help Menu (Pg. 3/3)", description="", color=discord.Color.green())
        em.add_field(name="The default prefix for the bot is `%`", value="""
        **Config commands**
        `Prefix <prefix>` - Changes the guilds prefix `(Aliases: SetPrefix)`
        `Checking <On|Off>` - Allows the use of the Done command `(No aliases)`
        `SetListName <New List Name>` - Changes the list name `(No aliases)`
        `Sort <alph|num> <ASC|DESC>` - Sorts list [alphabet/numer]ically ASC or DESC `(No aliases)`
        """, inline=True)
        em.set_footer(text="© 2021 Portal Development. All rights reserved -  `help <1 | 2 | 3>` for help")
    await ctx.send(embed=em)
for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        bot.load_extension(f'cogs.{filename[:-3]}') 


# Latest update 2.1.8
bot.run("Nzk4NzQ0MjYzOTU2ODg5NjAx.X_5ekA.5h94UI5FkZaouUJFtJKdmaKOYZg") 