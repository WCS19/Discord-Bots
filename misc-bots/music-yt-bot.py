import os
import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv

#Load opus library
filepath = os.getenv('OPUS_LIBRARY')
discord.opus.load_opus(filepath)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} is now online.')

@client.command(name='play', help='Plays a selected piece of music from YouTube')
async def play(ctx, *, search: str):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    channel = ctx.message.author.voice.channel

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'noplaylist': True,
        'quiet': True,
        'source_address': '0.0.0.0'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        URL = info['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(URL), after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {info["title"]}')

def run_bot():
    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()
