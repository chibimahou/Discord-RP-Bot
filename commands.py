import discord
from discord.ext import commands
from config.config import DISCORD_TOKEN

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"We have logged in as {bot.user}")

class DynamicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.command()
async def sync(self, ctx) -> None:
   fmt = await ctx.bot.tree.sync()
   await ctx.send(
      f"Synced {len(fmt)} command to the current guild."
   )
   return

bot.add_cog(DynamicCommands(bot))
bot.run(DISCORD_TOKEN)