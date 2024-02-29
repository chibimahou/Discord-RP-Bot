import discord
from discord.ext import commands

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

@bot.tree.command(name="addcommand")
@commands.has_permissions(administrator=True)  # Ensure only admins can add commands
async def add_command(self, interaction: discord.Interaction, command_name, *, response):
        if command_name in self.bot.all_commands:
            await ctx.send(f"A command with the name `{command_name}` already exists.")
            return

        @self.bot.command(name=command_name)
        async def dynamic_command(ctx):
            await ctx.send(response)

        await ctx.send(f"Command `{command_name}` added with response `{response}`.")

bot.add_cog(DynamicCommands(bot))
bot.run("MTAwNjM4NTMzNDEwOTYyMjMzNA.GPSUfe.jLjJd71L07Di1-W74hwM0VXQcCO-u2qJil6-oI")