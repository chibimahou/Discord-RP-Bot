import discord 
from cogs.utility import add_guild
from discord.ext import commands
from config.config import DISCORD_TOKEN
import os
import logging

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    cogs = ["cogs.moderation", "cogs.characters", "cogs.combat", "cogs.economy", "cogs.interactions", "cogs.inventory", "cogs.life_actions", "cogs.quests", "cogs.skills", "cogs.utility"]
    
    @bot.event 
    async def on_ready():
        logging.debug(f'Logged in as {bot.user.name}')

        #Get external commands   
        for cog in cogs:
            try:
                await bot.load_extension(cog)
                logging.debug(f"Loaded {cog}")
            except Exception as e:
                logging.exception(f"Failed to load {cog}: {e}")
        #sync with discord
        await bot.tree.sync()

    @bot.event
    async def on_guild_join(guild):
        logging.info(f"Joined a new guild: {guild.name}")
        add_guild(guild.id, guild.name)
            
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to run this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have the required permissions to run this command.")
        else:
            await ctx.send("An error occurred.")
            raise error
        
    bot.run(DISCORD_TOKEN)