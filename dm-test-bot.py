import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') 

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is now online.')

@client.command()
async def hello(message):
    await message.send('Hello, I am the bot')

@client.command()
async def senddm(ctx, user: discord.Member, *, message="Welcome to the server!"):  #* denots keyword only argument. message = value is default message if nothing provided
    embed = discord.Embed(title=message)
    await user.send(embed=embed)

def run_bot():
    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()
