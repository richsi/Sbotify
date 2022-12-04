import os
import discord
from discord.ext import commands
from discord import Interaction

intents = discord.Intents.all()
intents.message_content = True

TOKEN = "MTA0ODc3MTA2NjcxNTE4OTM0OA.G_x079.1BIEh2ZNBL0mmdLcexXukB1tXEPQxdN3ds0PMA"
BOT_PREFIX = "$"

intents = discord.Intents.all()
bot = commands.Bot(BOT_PREFIX, intents = discord.Intents.all())

#CLIENT
@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)

test_server = 910335283025805375
@bot.command(name = "ping", description="PONG", guild_ids=[test_server])
async def ping(ctx):
    await ctx.send("PONG")

#BOT
@bot.command(name = "join")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name = "leave")
async def leave(ctx):
    voice_channel = ctx.message.guild.voice_client
    await voice_channel.disconnect()




bot.run(TOKEN)
