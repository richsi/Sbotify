import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Spotify

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")
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
@bot.command()
async def song(ctx, user: discord.Member = None):
    user = user or ctx.author
    spotify_song = next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)

    for activity in user.activities:
        if isinstance(activity, Spotify):
            await ctx.send(
                f"{user} is listening to {activity.title} by {activity.artist}.\n")
    await ctx.send(f"https://open.spotify.com/track/{spotify_song.track_id}")
            
@bot.command()
async def gif(ctx, user: discord.Member = None):
    user = user or ctx.author
    


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
