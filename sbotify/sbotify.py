import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import Spotify
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import random
import requests
import json

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GIPHY_TOKEN = os.getenv("GIPHY_TOKEN")
TENOR_TOKEN = os.getenv("TENOR_TOKEN")

giphy_api_instance = giphy_client.DefaultApi()  #including giphy api token

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

#GIPHY
async def search_gifs_giphy(query):
    try:
        response = giphy_api_instance.gifs_search_get(GIPHY_TOKEN, query, limit=3, rating="g")
        gif_list = list(response.data)
        gif = random.choices(gif_list)
        return gif[0].url
    except ApiException as e:
        return "Exception when calling DefaultApi -> gifs_search_get: %s\n" %e

#TENOR
@bot.command()
async def search_tenor(ctx):
    apikey = str(TENOR_TOKEN)
    lmt = 7
    try:
        r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (ctx, apikey, lmt))
        data = r.json()
        return data['media'][0]['gif']['url']
        #return data['results'][0]['media'][0]['gif']['url'] 

    except ApiException as e:
        return "Exception when calling DefaultApi -> gifs_search_get: %s\n" %e

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
async def giphy(ctx, user: discord.Member = None):
    user = user or ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            search_input = activity.title + " " + activity.artist + " music"
            gif = await search_gifs_giphy(search_input)
            await ctx.send(f"GIF of {activity.artist}: \n" + gif)

# @bot.event
# async def tenor(ctx):
#     if ctx.author == bot.user:  #safety measures
#         return
#     user = user or ctx.author

#     if ctx.content.lower().startswith(f"{BOT_PREFIX}gif"):
#         gif_url = search_tenor(ctx.content.lower()[5:])

#         embed = discord.Embed()
#         embed.set_image(url=gif_url)
#         await ctx.channel.send(embed = embed)
            
@bot.command()
async def tenor(ctx):
    user = ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            search_input = activity.title + " " + activity.artist

            gif_url = await search_tenor(search_input)

            embed = discord.Embed()
            embed.set_image(url=gif_url)
            await ctx.channel.send(embed=embed)


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



bot.run(DISCORD_TOKEN)
