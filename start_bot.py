import discord 
from discord.ext import commands
from config.config import DISCORD_TOKEN
import logging

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    cogs = ["cogs.moderation", "cogs.characters", "cogs.combat", 
            "cogs.economy", "cogs.interactions", "cogs.inventory", 
            "cogs.life_actions", "cogs.quests", "cogs.skills", 
            "cogs.utility", "cogs.groups"]
    
    @bot.event
    async def on_ready():
        for cog in cogs:
            try:
                await bot.load_extension(cog)
                logging.info(f"Loaded {cog}")
            except Exception as e:
                logging.error(f"Failed to load {cog}: {e}")

        try:
            # Sync commands globally, consider handling per-guild during development
            await bot.tree.sync()
            logging.info('Successfully synced commands globally.')
        except Exception as e:
            logging.error(f'Error syncing commands: {e}')

        logging.info(f'Logged in as {bot.user.name}')
    
    bot.run(DISCORD_TOKEN)
