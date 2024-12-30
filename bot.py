from pyrogram import Client, filters
from pyrogram.errors import FloodWait 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time,os,json,sys
import asyncio
from helper.logprint import log

from configs import Configs
from translation import InlineKeyboard, Translation


#Initialise the bot
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

app.custom_data={'batch':False,"last_update_time":None}


'''#MAIN function
async def main():
    async with app:
        #print("Client started. Listening for messages...")
        print(f"\033[1;96m @Bot Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️\033[0m")
        #try:[await app.send_message(id,text='Hi This is userbot') for id in Configs.ADMIN]
        #except Exception as e:print('sending message error',e)
        try:
            await asyncio.Event().wait()  # Keeps the client running

        except KeyboardInterrupt:
            print("Client stopped due to keyboard interupt.")
        except:
            print(f"\033[1;96m Client stopped.\033[0m")


# Start the asyncio loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("An error occured.\n",e)'''


# Start the Bot
log('@Bot Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️')
app.run()