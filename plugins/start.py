from pyrogram import Client as Dmsbot
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.errors import FloodWait
import asyncio
from translation import Translation,InlineKeyboard 
import time,os,sys
from helper.logprint import log
from helper.database import CreateUser
from plugins.download import DownloadToServer,Download


@Dmsbot.on_message(filters.command(['start']))
async def start(client,message):
    #Register user in database
    CreateUser(message.from_user.id)
    log('Message Recieved')
    try:
        await message.reply(text=Translation.START,reply_markup=InlineKeyboard.START,reply_to_message_id=message.id)
    except FloodWait as t:
        asyncio.sleep(t)
    except Exception as e:
        print('An error occured',e)


@Dmsbot.on_message(filters.command(['help']))
async def help(client,message):
    client.custom_data['batch']=True
    log(client.custom_data.get('batch'))

