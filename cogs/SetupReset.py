import ast
import asyncio
import aiosqlite
import discord
import os
import time
from discord.ext import commands
from modules import module

class SetupReset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def setup(self, ctx):
        if ctx.guild.me.guild_permissions.manage_roles == False or ctx.guild.me.guild_permissions.manage_channels == False:
            embed = discord.Embed(title="Bot missing Permissions", description="To Run this command the bot needs the `Manage Roles` and `Manage Channels` permissions.", color=discord.Color.green())
            embed.set_footer(text=self.bot.footerText)
            await ctx.send(embed=embed)
        else:
            if await module.checkIfSetup(ctx.guild.id, self.bot):  
                embed=discord.Embed(title="This server has already been setup yet.", description="Please run the reset command if you wish to re-run the setup.", color=discord.Color.green())
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
                    await self.bot.db.execute(f"""INSERT INTO config
                    
                VALUES
                (
                {role1.id}, {role2.id}, {ctx.guild.id}, {updating_list.id}, {listChannel.id}, 'b', '{ctx.guild.name}s ToDo List', 1, 'pos ASC'
                )
                """)
                    await self.bot.db.commit()
                    errors.append(":white_check_mark: Updated the guild config database")
                except:
                    errors.append(":x: Failed to update the guild config database")
                test = '\n'.join(errors)
                em = discord.Embed(title="Setup Complete", description=f"The Setup was completed in {round(time.time() - startTime, 4)} seconds.", color=discord.Color.green())
                em.add_field(name="The following has been changed:", value=test)
                em.set_footer(text=self.bot.footerText)
                await ctx.send(embed=em)    


    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def reset(self, ctx):
        embed = discord.Embed(title=f"Please Confirm", description="Please react with :white_check_mark: to perform a full reset.", color=discord.Color.green())
        embed.set_footer(text=self.bot.footerText)
        message =  await ctx.send(embed=embed)
        await message.add_reaction("\U00002705")
        await message.add_reaction("\U0000274e")
        NotTimeout = True
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["\U00002705", "\U0000274e"]
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except:
            embed = discord.Embed(title="TimeOut Error", description="You did not react in time, reset cancelled.", color=discord.Color.green())
            embed.set_footer(text=self.bot.footerText)
            NotTimeout = False
            await ctx.send(embed=embed)
        if NotTimeout:
            if str(reaction.emoji) == "\U0000274e":
                embed = discord.Embed(title="Reset Cancelled", description="The reset was cancelled, no changes were made.", color=discord.Color.green())
                embed.set_footer(text=self.bot.footerText)
                await ctx.send(embed=embed)
            else:
                errors = []
                if await module.checkIfSetup(ctx.guild.id, self.bot):  
                    try:
                        ServerSetup = True
                        configInfo = await module.getconfiginfo(ctx.guild.id, self.bot)
                        print(configInfo)
                    except:
                        errors.append(":x: Could not fetch config info")
                        configInfo = [1,2,3,4,5]
            
                else:
                    ServerSetup = False
                if ServerSetup:
                    startTime = time.time()
                    channel = self.bot.get_channel(int(configInfo[4]))
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
                        await self.bot.db.execute(f"DELETE FROM config WHERE guildID = {ctx.guild.id}")
                        await self.bot.db.commit()
                        errors.append(":white_check_mark: Guild Config database deleted")
                    except:
                        errors.append(":x: Failed to delete the guild config-info database")
                    try:
                        await self.bot.db.execute(f"DELETE FROM items WHERE guildID = {ctx.guild.id}")
                        await self.bot.db.commit()
                        errors.append(":white_check_mark: List Items database deleted")
                    except:
                        errors.append(":x: Failed to delete the guild list-items database")
                    test = '\n'.join(errors)
                    em = discord.Embed(title="Reset Complete", description=f"The Reset was completed in {round(time.time() - startTime, 4)} seconds.", color=discord.Color.green())
                    em.add_field(name="The following has been changed:", value=test)
                    em.set_footer(text=self.bot.footerText)
                    await ctx.send(embed=em)                    
                    
                else:
                    embed=discord.Embed(title="This server has not been setup yet.", description="Please run the setup command before running this command.", color=discord.Color.green())
                    embed.set_footer(text=self.bot.footerText)
                    await ctx.send(embed=embed)
        else:
            return

def setup(bot):
    bot.add_cog(SetupReset(bot))