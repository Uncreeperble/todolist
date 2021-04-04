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
# Create a curosr
footerText = "© 2021 Portal Development. All rights reserved (%support)" #Displayed at the bottom of every message
NoPermissionMessage = discord.Embed(title=":warning: Error: No Permission", description="You do not have the required permissions to run this command", color=0x00a8ff) #error send when user does not have the required permissions to run the command.
NoPermissionMessage.set_footer(text=footerText)
NoRoleMessage = discord.Embed(title="Role Required", description="You require the `List Management` role to run this command", color=0x00a8ff) 
NoRoleMessage.set_footer(text=footerText)

c = conn.cursor()

def checkTableExists(tablename):
    a = True
    try:
        c.execute(f"""
            SELECT COUNT(*)
            FROM {tablename}
            """)
    
    except:
        a = False
    return a
def updateSequence(table):
    c.execute(f"SELECT rowid, * FROM {table}") # Get the row countt
    rows = c.fetchall()
    
    print(rows)
    done = []
    for a in range(len(rows)):
        print(a, done)
        if rows[a][0] not in done:
        
            done.append(rows[a][0])
            c.execute(f"UPDATE {table} SET sequence = {int(a+1)} WHERE rowid = {done[a]}")
            conn.commit()

    
  
@bot.command()
async def test(ctx):
    updateSequence(f"items{ctx.guild.id}")
@bot.command(aliases=['view'])
async def viewlist(ctx):
    print(f"{ctx.author.name} ran the command view")
    try:
        c.execute(f"SELECT ViewList FROM config{str(ctx.guild.id)}")

        rid = c.fetchone()[0]
    except:
        rid = 0
        print("rid = 0")
    if rid != 0: 
        role = ctx.guild.get_role(int(rid))
        if role in ctx.author.roles:
            c.execute(f"SELECT item, sequence FROM items{str(ctx.guild.id)}")
            list = c.fetchall()
            updateSequence(f"items{ctx.guild.id}")
            listI = []
            item_at = 0
            print(list)
            for i in range(len(list)):
                item_at += 1
                
                listI.append("**{}:** {} \n".format(list[i][1], list[i][0])) 
         
            try:     
                em = discord.Embed(title = f"{ctx.guild.name}'s To-Do List", description ="", color = 0x00a8ff)
                em.add_field(name=f"This server's list currently has {item_at} item/s.", value=''.join(listI), inline=False)
                em.set_footer(text=footerText)
                await ctx.send(embed=em)
            except:
                embed=discord.Embed(title="List Empty", description="The List has no items in it." ,color=0xf90101)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Role Required", description="You require the `View List` role to run this command", color=0x00a8ff) 
            embed.set_footer(text=footerText)
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=0x001eff)
        await ctx.send(embed=embed)
@bot.command(aliases=['add', 'add_item'])
async def additem(ctx, *, item = None):
    
    c.execute(f"""INSERT INTO items{str(ctx.guild.id)} VALUES ("{str(item)}", 0)""")
    conn.commit()
    updateSequence(f"items{ctx.guild.id}")
    embed=discord.Embed(title="Item Added", description=f"`{item}` has been added to {ctx.guild.name}'s To-Do List.", color=0x04ff00)
    embed.set_footer(text=footerText)    
    await ctx.send(embed=embed)
    c.execute(f"""SELECT updatingMSG FROM config{str(ctx.guild.id)}""")
    a = c.fetchall()
    updating_list = a[0][0]
    c.execute(f"SELECT updatingChannel FROM config{str(ctx.guild.id)}")
    a = c.fetchall()
    ab = a[0][0]
    channel = bot.get_channel(ab)
    msg = await channel.fetch_message(updating_list)
    await msg.delete()
    
    c.execute(f"SELECT item, sequence FROM items{str(ctx.guild.id)}")
    list = c.fetchall()
    
    listI = []
    item_at = 0
  
    for i in list:
        print(i)
        item_at += 1
        listI.append("**{}:** {} \n".format(item_at, i[0])) 
    try:           
        em = discord.Embed(title = f"{ctx.guild.name}'s To-Do List", description ="", color = 0x00a8ff)
        em.add_field(name=f"This server's list currently has {item_at} item/s.", value=''.join(listI), inline=False)
        em.set_footer(text=footerText)
        updating_list = await channel.send(embed=em)
    except:
        embed=discord.Embed(title="List Empty", description="The List has no items in it." ,color=0x00a8ff)
        updating_list = await channel.send(embed=em)
  
    c.execute(f"UPDATE config{str(ctx.guild.id)} SET updatingMSG = {updating_list.id}")
    conn.commit()
 
    updateSequence('items{ctx.guild.id}')
           

bot.run("Nzk4NzQ0MjYzOTU2ODg5NjAx.X_5ekA.5h94UI5FkZaouUJFtJKdmaKOYZg") 
