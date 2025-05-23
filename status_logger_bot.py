from dotenv import load_dotenv
load_dotenv()
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Replace with your actual log channel ID
LOG_CHANNEL_ID = 1375401157471502437  # <- Put your channel ID here

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

# Replace 'YOUR_BOT_TOKEN' with your bot token
import os
bot.run(os.getenv('YOUR_BOT_TOKEN'))

