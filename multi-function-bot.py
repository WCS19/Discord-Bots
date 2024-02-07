import os
import discord
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True  

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} is now online.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello') or message.content.startswith('hello'):
        await message.channel.send('Hello! I am a test bot.')

    elif message.content.startswith('!weather'):
        city = message.content.split(' ', 1)[1]
        await get_weather(message.channel, city)

    elif message.content.startswith('!poll'):
        options = message.content.split(' ')[1:]
        await create_poll(message.channel, options)

#Welcome message function
@client.event
async def on_member_join(member):
    welcome_channel_id = os.getenv('CHANNEL_ID') 
    welcome_message = f"Welcome to the server, {member.mention}! Feel free to introduce yourself."
    channel = client.get_channel(welcome_channel_id)
    if channel:
        await channel.send(welcome_message)

#Weather function
async def get_weather(channel, city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_desc = data['weather'][0]['description']
        temp_fahrenheit = round(data['main']['temp'])
        feels_like_fahrenheit = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        wind_speed_mph = round(data['wind']['speed'])

        await channel.send(f'{city} weather is currently {weather_desc}. '
                           f'The current temperature is {temp_fahrenheit}°F and feels like {feels_like_fahrenheit}°F. '
                           f'Current humidity is {humidity}%, with wind speeds of {wind_speed_mph} mph.')
    else:
        await channel.send(f'Error: Unable to retrieve weather for "{city}".')

#Poll function
async def create_poll(channel, options):
    if len(options) < 2:
        await channel.send('Please provide at least two options for the poll')
        return
    if len(options) > 10:
        await channel.send('Maximum number of options allowed is 10')
        return
    formatted_options = '\n'.join([f'{i+1}. {option}' for i, option in enumerate(options)])
    poll_message = await channel.send(f'**Poll:**\n{formatted_options}')
    for i in range(len(options)):
        await poll_message.add_reaction(chr(127462 + i))




client.run(TOKEN)
