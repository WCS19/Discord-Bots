# Custom Discord Bots

As a frequent user of discord I wanted to create a variety of discord bots that have different and unique functionality. This repository contains a collection of custom Discord bots that I am working on, each designed with unique functionalities aimed at enhancing Discord's server experience. The bots include an initial test bot for basic operations/an initial setup, a multi-function bot(weather, reminders, & polls), a reminder bot, and a youtube audio bot. This README will guide you through the setup, configuration, and usage of these bots.

## Overview of Bots

- **Initial Test Bot**: A basic bot setup to test server connection and command message parsing.
- **Multi-Function Bot**: A versatile bot integrating various features for server management, user engagement, and more.
- **Reminder Bot**: Capable or creating, deleting, and storing scheduled reminders each with unique IDs for logging and reminder storage management.
- **Music-Test Bot**: An experimental bot designed to test music playback features within Discord.
- **Music-YouTube Bot**: Streams music from YouTube to Discord voice channels.


## Prerequisites

Before setting up the bots, ensure you have the following:

- [Python](https://www.python.org/downloads/) (3.8 or newer recommended)
- [pip](https://pip.pypa.io/en/stable/installation/) for managing Python packages
- A Discord account and access to a server where you can add bots

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
```.txt
DISCORD_TOKEN = <Your_Discord_Bot_TOKEN>
```

### Step 4: Invite Bot/s to Your Server

For each bot, you need to invite them to your Discord server. Use the Discord Developer 
Portal to create bot users and gerneate invite links with appropriate permissions.

### Usage

Once the bots are added to your server and running, you can interact with them using their specific commands. For example:

Use !play <YouTube_Video_Link> or <'song name, artist name'> to play music from YouTube in a voice channel with the Music-YouTube Bot.

Refer to each bot's command list for more details on available commands and functionalities.

### Contributing
Contributions to improve the bots or add new features are welcome. Please follow the standard fork-and-pull request workflow.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgements

Special thanks to all contributors and the open-source projects that made these bots possible. These 
bots were inspired by John Crickett's [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-discord)