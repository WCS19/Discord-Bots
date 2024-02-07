import os
import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv

# Load Opus library
discord.opus.load_opus('/opt/homebrew/opt/opus/lib/libopus.dylib')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
#this works just bad quality
# @bot.command(name='play', help='Plays a selected piece of music from YouTube')
# async def play(ctx, *, search: str):
#     if not ctx.message.author.voice:
#         await ctx.send("You are not connected to a voice channel")
#         return

#     channel = ctx.message.author.voice.channel

#     if ctx.voice_client is not None:
#         if ctx.voice_client.is_playing():
#             ctx.voice_client.stop()
#         await ctx.voice_client.move_to(channel)
#     else:
#         await channel.connect()

#     ydl_opts = {
#     'format': 'bestaudio/best',
#     'default_search': 'ytsearch',
#     'noplaylist': True,
#     'quiet': True,
#     'source_address': '0.0.0.0',
#     'format_options': {
#         'audio_quality': '320k',  # Adjust the audio quality as desired (e.g., 320k, 256k, etc.)
#         'audio_bitrate': 320000,  # Adjust the audio bitrate as desired (e.g., 320000, 256000, etc.)
#     },
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',  # Extract audio using FFmpeg
#         'preferredcodec': 'mp3',  # Preferred audio codec (e.g., mp3, m4a, opus)
#         'preferredquality': '320',  # Preferred audio quality (e.g., 320 for MP3)
#     }],
# }


#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
#         URL = info['url']
#         ctx.voice_client.play(discord.FFmpegPCMAudio(URL), after=lambda e: print(f'Player error: {e}') if e else None)
#         await ctx.send(f'Now playing: {info["title"]}')
@bot.command(name='play', help='Plays a selected piece of music from YouTube')
async def play(ctx, *, search: str):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    channel = ctx.message.author.voice.channel

    if ctx.voice_client is not None:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'noplaylist': True,
        'quiet': True,
        'source_address': '0.0.0.0',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        URL = info['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(URL, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', options='-vn'), after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(f'Now playing: {info["title"]}')

bot.run(TOKEN)
