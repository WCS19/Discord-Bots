import os
import asyncio
import difflib
import uuid
import discord
import logging
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

from discord.ext.commands import has_permissions, CheckFailure

#Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Discord client with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

# Disable the default help command
client.remove_command('help')

class Ticket:
    def __init__(self, id, message, user):
        self.id = id
        self.message = message
        self.user = user

tickets = {}  #empty dictionary to store tickets

def closest_command(user_input, command_list):
    matches = difflib.get_close_matches(user_input, command_list, n=1, cutoff=0.6)
    # setting n=1 produces only the top match
    # setting cutoff=0.6 only considers matches above 60%
    return matches[0] if matches else None

@client.event
async def on_ready():
    print(f'{client.user} is now online.')
    channel_id = os.getenv('CHANNEL_ID')
    if channel_id:
        channel = client.get_channel(int(channel_id))
        if channel:
            await channel.send('Hi there! I am the Ticket Bot. Please use `!help` for a list of possible commands.')
        else:
            print(f'Could not find a channel with ID: {channel_id}')
    else:
        print('No CHANNEL_ID found in environment variables.')

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
async def help_command(ctx):
    # Default help message for normal users
    help_message = '''
**Bot Commands:**
| `!ticket <message>`: Creates a ticket with the specified message.
| `!showmytickets`: Lists all the current tickets you have created.
| `!cancelticket <ID>`: Cancels the ticket with the specified ID.
| `!help`: Displays this help message with a list of available commands.
'''

    # Check if the user has the Administrator permission
    if ctx.message.author.guild_permissions.administrator:
        # Add the admin-specific command to the help message
        admin_help = '''
| `!resolveticket <ID>`: Resolves the ticket with the specified ID. (Admin Only)
| `!addusertochannel <ID>`: Adds the user who created the specified ticket to a private channel. (Admin Only)
'''
        help_message += admin_help  # Append admin commands to the help message

    await ctx.send(help_message)

@client.command(name='ticket', help='Creates a ticket with the specified message.')
async def create_ticket(ctx, *, message: str):
    ticket_id = str(uuid.uuid4())
    tickets[ticket_id] = Ticket(ticket_id, message, ctx.author)

    # Send DM to the user who created the ticket
    try:
        dm_message = f"Your ticket has been created! Your ticket ID is {ticket_id}.\nTicket message: \"{message}\""
        await ctx.author.send(dm_message)
        confirmation_message_user = f"{ctx.author.mention}, your ticket has been created. Check your DMs for details."
    except discord.Forbidden:
        confirmation_message_user = (f"{ctx.author.mention}, your ticket has been created, but I couldn't send you a DM. "
                                     "Please check your privacy settings or DM me first so I can reply with your ticket details.")
    await ctx.send(confirmation_message_user)

    # Send ticket info to the private channel for admins
    admin_channel_id = os.getenv('ADMIN_CHANNEL_ID')
    admin_channel = client.get_channel(int(admin_channel_id))
    if admin_channel:
        admin_message = f"New ticket created by {ctx.author.mention}:\nTicket ID: {ticket_id}\nTicket message: \"{message}\""
        await admin_channel.send(admin_message)

@client.command(name='showmytickets', help='Lists all the current tickets you have created.')
async def show_user_tickets(ctx):
    await show_tickets(ctx.author)

async def show_tickets(user):
    user_tickets = [ticket for ticket in tickets.values() if ticket.user == user]
    if user_tickets:
        ticket_list = '\n'.join([f'Ticket ID: {ticket.id}: {ticket.message}' for ticket in user_tickets])
        dm_message = f'Your tickets:\n{ticket_list}'
    else:
        dm_message = 'You have no tickets.'

    try:
        await user.send(dm_message)
        await user.guild.system_channel.send(f"{user.mention}, I've sent you a DM with your existing tickets.")

    except discord.Forbidden:
        # Fallback message in case the bot can't send DMs to the user
        fallback_message = (f"{user.mention}, I couldn't send you a DM. "
                            "Please check your privacy settings or DM me first so I can reply with your ticket details.")
        await user.guild.system_channel.send(fallback_message)

@client.command(name='cancelticket', help='Cancels the ticket with the specified ID.')
async def cancel_ticket_command(ctx, ticket_id: str):
    await cancel_ticket(ctx, ticket_id)

async def cancel_ticket(ctx, ticket_id):
    ticket = tickets.pop(ticket_id, None)
    if ticket:
        await ctx.send(f'Ticket {ticket_id} has been cancelled.')
    else:
        await ctx.send(f'No ticket found with ID: {ticket_id}')

@client.command(name='resolveticket', help='Resolves a specified ticket.', hidden=True)
@has_permissions(administrator=True)  # Ensures only users with the administrator permission can use this command
async def resolve_ticket(ctx, ticket_id: str):
    # Check if the ticket exists
    ticket = tickets.pop(ticket_id, None)
    if ticket:
        # Logic to mark the ticket as resolved or to delete it
        await ctx.send(f'Ticket {ticket_id} resolved by {ctx.author.mention}.')
        # Optionally, notify the ticket creator if needed
        await ticket.user.send(f'Your ticket with ID {ticket_id} has been resolved by {ctx.author.mention}.')
    else:
        await ticket.user.send(f'Your ticket with ID {ticket_id} has been resolved by {ctx.author.mention}.')

@resolve_ticket.error  # This handles any errors from the resolve_ticket command
async def resolve_ticket_error(ctx, error):
    if isinstance(error, CheckFailure):  # This checks if the error was because of failed permission checks
        await ctx.send('You do not have permission to use this command.')
    else:
        print(f"An error occurred: {error}")

#NOT YET WORKING.
@client.command(name='addusertochannel', help='Adds the user who created the specified ticket to a private channel. (Admin Only)', hidden=True)
@has_permissions(administrator=True)
async def add_user_to_channel(ctx, ticket_id: str):
    # Check if the ticket exists
    ticket = tickets.get(ticket_id)
    if ticket:
        user = ticket.user
        private_channel_id = os.getenv('PRIVATE_CHANNEL_ID')
        private_channel = client.get_channel(int(private_channel_id))

        # Check if the private channel is found and is a TextChannel
        if private_channel and isinstance(private_channel, discord.TextChannel):
            # Add the user to the private channel
            await private_channel.set_permissions(user, read_messages=True, send_messages=True)
            # await ctx.send(f'{user.mention} has been added to {private_channel.mention}.')
            await user.send(f'You have been added to {private_channel.name} for ticket discussion.')
        else:
            await ctx.send('Private channel not found or is not a text channel.')
    else:
        await ctx.send(f'No ticket found with ID: {ticket_id}.')


def run_bot():
    client.run(TOKEN)

if __name__ == '__main__':
    run_bot()