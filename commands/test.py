import discord
from discord.ext import commands, tasks

class TestCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx: commands.Context):
        await ctx.send(f"Hey {ctx.author.mention}! This is a slash command!")

def setup(bot):
    bot.add_cog(TestCommand(bot))
