
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 

#Initialize intents
intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True  
intents.reactions = True 

#Initialize client and command prefix
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is now online.')

@client.command()
async def hello(message):
    if message.author == client.user:
        return   
    await message.send('Hello, I am a test bot.')

def run_bot():
    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()

