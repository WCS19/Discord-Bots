import asyncio
from datetime import datetime
from discord.ext import commands
import uuid
import os
import discord
import logging
import re
from dotenv import load_dotenv
import difflib

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
client = commands.Bot(command_prefix='!', intents=intents)

#Disable the default help command
client.remove_command('help')

class Reminder:
    def __init__(self, id, time, message, task):
        self.id = id
        self.time = time
        self.message = message
        self.task = task

reminders = {}  #empty dictionary to store reminders

        
def closest_command(user_input, command_list):
    # Use get_close_matches to find the closest match
    matches = difflib.get_close_matches(user_input, command_list, n=1, cutoff=0.6)
    # setting n=1 produces only the top match
    # setting cutoff=0.6 only considers matches above 60%
    return matches[0] if matches else None


@client.event
async def on_ready():
    print(f'{client.user} is now online.')
    channel_id = os.getenv('CHANNEL_ID')
    if channel_id:
        channel_id = int(channel_id)  
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send('Hi there! I am the Reminder Bot. Please use `!help` for a list of possible commands.')
        else:
            print(f'Could not find a channel with ID: {channel_id}')
    else:
        print('No CHANNEL_ID found in environment variables.')
        
        
@client.event
async def on_message(ctx):
    print(f'Received message from {ctx.author}: {ctx.content}') #console logging for debugging
    if ctx.author == client.user:
        return
    await client.process_commands(ctx)
    
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Extract the attempted command name from the error message
        attempted_command = str(error).split('"')[1]
        command_list = [command.name for command in client.commands]
        suggestion = closest_command(attempted_command, command_list)
        if suggestion:
            await ctx.send(f"Command not found. Did you mean `!{suggestion}`? Please check `!help` for the list of available commands.")
        else:
            await ctx.send("Command not found. Please check `!help` for the list of available commands.")
    else:
        print(f"An error occurred: {error}")
        
        
@client.command(name='help', help='Displays the help message with a list of available commands.')
async def custom_help(ctx, *, command_name=None):
    """A custom help command."""
    if command_name:
        #Try to find a match among the bot's existing commands
        command = discord.utils.find(lambda c: c.name == command_name, client.commands)
        if command:
            help_message = f'**{command.name} Command:**\n{command.help}'
            await ctx.send(help_message)
        else:
            await ctx.send(f'No command named "{command_name}" found.')
    else:  #If no specific command is requested, show general help
        help_message = '''
        **Reminder Bot Commands:**
        | `!reminder YYYY-MM-DD HH:MM <message>`: Sets a reminder with the specified message at the given date and time.
        | `!showreminders`: Lists all the current reminders set by users.
        | `!cancelreminder <ID>`: Cancels the reminder with the specified ID.
        | `!help`: Displays this help message with a list of available commands.
        '''
        await ctx.send(help_message)
        
        
@client.command(name='reminder', help='Sets a reminder with the specified message at the given date and time.')
async def reminder(ctx, *, command_input):
    await set_reminder(ctx.channel, command_input)

async def remind(channel, reminder):
    await asyncio.sleep((reminder.time - datetime.now()).total_seconds())
    await channel.send(reminder.message)
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
    await channel.send(f"Reminder set! I will remind you to '{reminder_msg}' at {time_str} on {date_str} .")
    
    
@client.command(name='showreminders', help='Lists all the current reminders set by users.')
async def showreminders(ctx):
    if reminders:
        reminders_list = []
        for reminder_id, reminder in reminders.items():
            time_str = reminder.time.strftime('%Y-%m-%d %H:%M')
            reminders_list.append(f"ID: {reminder_id}, Time: {time_str}, Message: '{reminder.message}'")
        reminders_message = "\n".join(reminders_list)
        await ctx.channel.send(f"Current Reminders:\n{reminders_message}")
    else:
        await ctx.channel.send("There are no scheduled reminders.")
        
        
@client.command(name='cancelreminder', help='Cancels the reminder with the specified ID.')
async def cancelreminder(ctx, reminder_id):
    reminder = reminders.pop(reminder_id, None)
    if reminder:
        reminder.task.cancel()
        await ctx.channel.send(f"Reminder with ID {reminder_id} has been cancelled.")
    else:
        await ctx.channel.send(f"No reminder found with ID {reminder_id}.")

async def cancel_reminder(reminder_id):
    reminder = reminders.pop(reminder_id, None)
    if reminder:
        reminder.task.cancel()
    else:
        print(f'Message not found, reminder can be sent here')


def run_bot():
    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()
