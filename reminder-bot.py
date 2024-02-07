import asyncio
from datetime import datetime
# from datetime import timedelta
import uuid
import os
import discord
# import requests
import logging
import re
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

class Reminder:
    def __init__(self, id, time, message, task):
        self.id = id
        self.time = time
        self.message = message
        self.task = task

reminders = {}  #empty dictionary to store reminders

async def remind(channel, reminder):
    await asyncio.sleep((reminder.time - datetime.now()).total_seconds())
    await channel.send(reminder.message)
    # Remove the reminder from the dictionary
    reminders.pop(reminder.id, None)

async def set_reminder(channel, command_input):
    match = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) (.+)", command_input)
    if not match:
        await channel.send("Invalid command format. Please use '!reminder YYYY-MM-DD HH:MM Your reminder message.'")
        return

    date_str, time_str, reminder_msg = match.groups()
    try:
        reminder_time = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        if reminder_time <= datetime.now():
            await channel.send("Reminder time must be in the future.")
            return
    except ValueError:
        await channel.send("Invalid time format. Please use 'YYYY-MM-DD HH:MM'.")
        return

    reminder_id = str(uuid.uuid4())
    task = asyncio.create_task(remind(channel, Reminder(reminder_id, reminder_time, reminder_msg, None)))
    reminders[reminder_id] = Reminder(reminder_id, reminder_time, reminder_msg, task)
    await channel.send(f"Reminder set with ID {reminder_id}. I will remind you to '{reminder_msg}' at {date_str} {time_str}.")

async def cancel_reminder(reminder_id):
    reminder = reminders.pop(reminder_id, None)
    if reminder:
        reminder.task.cancel()
        # print(f'Reminder {reminder_id} has been cancelled')
    else:
        print(f'Message not found, reminder can be sent here')

@client.event
async def on_ready():
    print(f'{client.user} is now online.')

@client.event
async def on_message(message):
    if message.content.startswith('!reminder'):
        command_input = message.content[len('!reminder '):].strip()
        await set_reminder(message.channel, command_input)
    elif message.content.startswith('!showreminders'):
        if reminders:
            reminders_list = []
            for reminder_id, reminder in reminders.items():
                time_str = reminder.time.strftime('%Y-%m-%d %H:%M')
                reminders_list.append(f"ID: {reminder_id}, Time: {time_str}, Message: '{reminder.message}'")
            reminders_message = "\n".join(reminders_list)
            await message.channel.send(f"Current Reminders:\n{reminders_message}")
        else:
            await message.channel.send("There are no scheduled reminders.")
    elif message.content.startswith('!cancelreminder'):
        # Extract the reminder ID from the command
        parts = message.content.split(' ')
        if len(parts) < 2:
            await message.channel.send("Please provide the reminder ID.")
            return

        reminder_id = parts[1]

        # Attempt to cancel the reminder
        reminder = reminders.pop(reminder_id, None)
        if reminder:
            reminder.task.cancel()
            await message.channel.send(f"Reminder with ID {reminder_id} has been cancelled.")
        else:
            await message.channel.send(f"No reminder found with ID {reminder_id}.")

# Start the bot
client.run(TOKEN)
