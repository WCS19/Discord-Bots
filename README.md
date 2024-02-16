# Custom Discord Bots

As a frequent user of discord I wanted to create a variety of discord bots that have different and unique functionality. This repository contains a collection of custom Discord bots that I am working on, each designed with unique functionalities aimed at enhancing Discord's server experience. The bots include an initial test bot for basic operations/an initial setup, a direct message test bot for testing direct messagine capability, a support ticket management bot, a reminder bot, a youtube audio streaming bot, and a multi-function bot(currently developing feature set). This README will guide you through the setup, configuration, and usage of these bots.

## Overview of Bots

- **Initial Test Bot**: A basic bot setup to test server connection and command message parsing.
- **DM Functionality Test Bot**: A basic bot that sends a direct message to a user once they first join the server. 
- **Ticket Management Bot**: Aids discord admins in the creation, resolution, and management of discord sever support tickets.
- **Reminder Bot**: Capable or creating, deleting, and storing scheduled reminders each with unique IDs for logging and reminder storage management.
- **Music-YouTube Bot**: Streams music from YouTube to Discord voice channels (still working on audio quality).
- **Multi-Function Bot**: This bot is being worked on now. The aim is to aid server admin with permissions, support tickets, moderation, etc.




## Prerequisites

Before setting up the bots, ensure you have the following:

- [Python](https://www.python.org/downloads/) (3.8 or newer recommended)
- [pip](https://pip.pypa.io/en/stable/installation/) for managing Python packages
- A [Discord Account](https://discord.com/), [Discord Developer Portal Account](https://discord.com/developers/docs/intro), and access to a server where you can add bots

## Installation

Follow these steps to get the bots up and running on your server:

### Step 1: Clone the Repository


Clone this repository to your local machine using:

```bash
git clone https://github.com/WCS19/discordbot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

For the music-yt bot, FFmpeg and Opus are required for audio processing and voice support in Discord bots. Since these cannot be installed via `pip`, MacOS users can install FFmpeg and Opus using Homebrew.

```bash
brew install ffmpeg
```
```bash
brew install opus
```
### Step 3: Configure Enviornment Variables
Create a .env file and populate the following fields:
```.txt
DISCORD_TOKEN = <Your-Discord-Bot-TOKEN>
```
*The Discord Token is required for all bots.*

```.txt
CHNNEL_ID = <Your-General-Channel-ID>
```

```.txt
ADMIN_CHANNEL_ID = <Your-Admin-Only-Discord-Channel-ID>
```

```.txt
OPUS_LIBRARY = <filepath/to/your/opus/library/>
```
*The Music-YT bot is the only bot using the Opus library*

### Step 4: Invite Bot/s to Your Server

For each bot, you need to invite them to your Discord server. Use the Discord Developer 
Portal to create bot users and gerneate invite links with appropriate permissions (admin recommended; however, grant permission according to your use case).

### Usage

Once the bots are added to your server and running, you can interact with them using their specific commands. For example:

Use !ticket <support message/ request to be sent to admins> to create a support ticket.

Refer to each bot's command list for more details on available commands and functionalities. All bots use custom !help commands to display both genral permission commands and admin only commands.

### Contributing
Contributions to improve the bots or add new features are welcome. Please follow the standard fork-and-pull request workflow.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgements

Thank you for visiting my Discord Bots Project repository. These bots were inspired by John Crickett's [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-discord)
