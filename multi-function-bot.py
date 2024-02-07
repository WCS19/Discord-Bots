import os
import discord
from dotenv import load_dotenv
import requests
from datetime import datetime
import asyncio

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

    if message.content.startswith('!hello') or message.content.startswith('hello'):
        print("Match found for '!hello/hello', sending response...")  # Debug print
        await message.channel.send('Hello! I am a test bot.')

    elif message.content.startswith('!weather'):
        city = message.content.split(' ', 1)[1]
        await get_weather(message.channel, city)

    elif message.content.startswith('!poll'):
        options = message.content.split(' ')[1:]
        await create_poll(message.channel, options)

    # elif message.content.startswith('!reminder'):
    #     parts = message.content.split(' ', 2)
    #     time_str = parts[1]
    #     reminder_msg = parts[2]
    #     await set_reminder(message.channel, time_str, reminder_msg)

#Weather function
async def get_weather(channel, city):
    api_key = os.getenv('OPENWEATHER_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        weather_desc = data['weather'][0]['description']
        temp_fahrenheit = round(data['main']['temp'])
        feels_like_fahrenheit = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        wind_speed_mph = round(data['wind']['speed'])

        await channel.send(f'The weather in {city} is {weather_desc}. '
                           f'Temperature: {temp_fahrenheit}°F (Feels like: {feels_like_fahrenheit}°F), '
                           f'Humidity: {humidity}%, Wind Speed: {wind_speed_mph} mph')

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

#Reminder function (still working on)
# async def set_reminder(channel, time_str, reminder_msg):
#     try:
#         reminder_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M')
#         now = datetime.now()
#         if reminder_time <= now:
#             await channel.send('Reminder time must be in the future')
#             return
#         delta = (reminder_time - now).total_seconds()
#         await asyncio.sleep(delta)
#         await channel.send(f'Reminder: {reminder_msg}')
#     except ValueError:
#         await channel.send('Invalid time format. Please use YYYY-MM-DD HH:MM')

client.run(TOKEN)
