from pyrogram import Client as Dmsbot
from pyrogram import filters
from pyrogram.errors import FloodWait 
from translation import Translation,InlineKeyboard
from helper.logprint import log
from helper.others import message_type
import asyncio
from plugins.download import Download,BatchDownload
from pyrogram.types import CallbackQuery
from plugins.upload import uploadToDms
from configs import Configs

@Dmsbot.on_message(filters.private & filters.document|filters.video|filters.audio|filters.photo)
async def main(client,message):
    log(f'{message_type(message)} recieved')

    try: 
        if client.custom_data.get('batch'):#GetBatchFlag(message.from_user.id):
            await BatchDownload(client,message)
        else:
            await message.reply(Translation.DOWNLOAD,reply_to_message_id=message.id,reply_markup=InlineKeyboard.DOWNLOAD)
    except FloodWait as t:
        asyncio.sleep(t)
    except Exception as e:
        pass
    
