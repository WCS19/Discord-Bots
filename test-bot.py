
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 

intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True  
intents.reactions = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is now online.')

@client.event
async def on_message(message):
    print(f"Received message from {message.author}: {message.content}")  # Debug print
    if message.author == client.user:
        return

    if message.content == '!hello' or message.content =='hello':
        print("Match found for '!hello/hello', sending response...")  # Debug print
        await message.channel.send('Hello! I am a test bot.')

client.run(TOKEN)

