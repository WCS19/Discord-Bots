import os
import discord
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is now online.')



def run_bot():
    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()
