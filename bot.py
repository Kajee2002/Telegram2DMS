from pyrogram import Client, filters
from pyrogram.errors import FloodWait 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import asyncio
import os
from helper.logprint import log

from configs import Configs
from translation import InlineKeyboard, Translation

# Initialize the bot
app = Client(
    "DMSBot",
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN,
    workers=min(32, os.cpu_count() + 4),
    plugins={"root": "plugins"},
    sleep_threshold=15,
    max_concurrent_transmissions=Configs.MAX_CONCURRENT_TRANSMISSIONS,
)

app.custom_data = {'batch': False, "last_update_time": None}

# Flask app for web service
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "Bot is running!"

# Function to run the bot
async def run_bot():
    log('@Bot Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️')
    await app.start()  # Use asyncio to start the bot

if __name__ == "__main__":
    # Run the bot in the main thread using asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    # Start the Flask web server in a separate thread
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=8080)).start()

    # Run the asyncio event loop
    loop.run_forever()
