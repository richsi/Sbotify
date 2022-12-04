import os
import nextcord
from discord.ext import commands

TOKEN = "MTA0ODc3MTA2NjcxNTE4OTM0OA.Gn9yKd.PsCa3mZ-DIhybD-YzgLosSaCRLDVQ3DDAxmD-8"
BOT_PREFIX = "$"

bot = commands.Bot(command_prefix = BOT_PREFIX)

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")


bot.run(TOKEN)
