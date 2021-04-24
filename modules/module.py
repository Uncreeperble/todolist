import discord
import aiosqlite


async def getconfiginfo(id, bot):
    print(5)
    e = await bot.db.execute(f"SELECT * FROM config WHERE guildID = {id}")
    configInfo = list(e[0][0])
    return configInfo


async def checkIfSetup(guildID, bot):
    cursor = await bot.db.execute(f"""
        SELECT count(*)
        FROM config WHERE guildID = {guildID}
        """)
    config = await cursor.fetchone()
    if str(config) != "(0,)":
        return True
    return False
    
async def updatePos(ctx, bot):
    guildID = ctx.guild.id
    test = await bot.db.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
    amt = int(test[0])
    sorti = await bot.db.execute(f"SELECT sort FROM config WHERE guildID = {guildID}")
    sort = sorti[0]

    if amt != 0:
        items = await bot.db.execute(f"SELECT * FROM items WHERE guildID = {guildID} ORDER BY {sort}")
        await bot.db.execute(f"DELETE FROM items WHERE guildID = {guildID}")
        for i in range(amt):
            await bot.db.execute(f"""INSERT INTO items VALUES 
            ({ctx.guild.id}, "{items[i][1]}", {i+1}, 0)
        """)
            await bot.db.commit()
    else:
        return

async def updateList(ctx, em, bot):
    configInfo = getconfiginfo(ctx.guild.id, bot)
    channel = bot.get_channel(int(configInfo[4]))
    msg = await channel.fetch_message(int(configInfo[3]))
    await msg.delete()
    newMSG = await channel.send(embed=em)
    await bot.db.execute(f"""UPDATE config SET updatingMSG = {int(newMSG.id)} WHERE guildID = {ctx.guild.id}""")
    await bot.db.commit()
async def generateListEM(ctx, bot):
    e = await bot.db.execute(f"SELECT * FROM config WHERE guildID = {ctx.guild.id}")
    configInfo = list(e[0][0])
    guildID = ctx.guild.id
    a = await bot.db.execute(f"SELECT COUNT(*) FROM items WHERE guildID = {guildID}")
    upto = int(a[0][0])
    b = await bot.db.execute(f"SELECT sort FROM config WHERE guildID = {guildID}")
    sort = b[0][0]
    G = bot.get_guild(int(guildID))
    GNAME = G.name
    if upto != 0:
        items = await bot.db.execute(f"SELECT * FROM items WHERE guildID = {guildID} ORDER BY {sort}")
        SplitList = ""
        c = await bot.db.execute(f"SELECT listName FROM config WHERE guildID = {guildID}")
        lname = c[0][0]
        d = await bot.db.execute(f"SELECT enableChecking FROM config WHERE guildID = {guildID}")
        checking = d[0][0]
        if checking == 0:
            for i in range(upto):
                if items[i][3] == 0:
                    SplitList = SplitList + f"\n <:DND:711874983726547005>[{items[i][2]}] {items[i][1]}"
                else:
                    SplitList = SplitList + f"\n <:online:711875039087165480>[{items[i][2]}] {items[i][1]}"
        else:   
            for i in range(upto):
                SplitList = SplitList + f"\n [{items[i][2]}] {items[i][1]}"
        em = discord.Embed(title = f"{lname}", description ="", color = discord.Color.green())
        em.add_field(name=f"This server's list currently has {upto} item/s (ID | Item).", value=SplitList, inline=False)
        em.set_footer(text=ctx.bot.footerText)
    else:
        em = discord.Embed(title = f"{GNAME}'s To-Do List", description ="", color = discord.Color.green())
        em.add_field(name=f"No items to be displayed.", value="`AddItem <Item>`", inline=False)
        em.set_footer(text=ctx.bot.footerText)
    return em  
