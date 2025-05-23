import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables from .env file
load_dotenv()

# Get the bot token
TOKEN = os.getenv('YOUR_BOT_TOKEN')
if TOKEN is None:
    raise ValueError("❌ Bot token not found. Set 'YOUR_BOT_TOKEN' in your .env file or hosting environment.")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Channel to log messages and presence updates
LOG_CHANNEL_ID = 1375401157471502437  # <- Your Discord log channel ID

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.event
async def on_presence_update(before, after):
    if before.status != after.status:
        channel = bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(
                f"🟡 **{after.name}** status change: `{before.status}` → `{after.status}`"
            )

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(
            f"💬 **{message.author}** said in **#{message.channel}**: {message.content}"
        )

    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
