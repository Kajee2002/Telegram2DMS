from pyrogram import Client as Dmsbot
from pyrogram.types import CallbackQuery
from translation import Translation,InlineKeyboard
from helper.logprint import log
from plugins.download import DownloadToServer,Download
from pyrogram import filters

@Dmsbot.on_callback_query(filters.regex(r'^(?!.*dmslogin).*'))
async def callback(client,query:CallbackQuery):
    data=query.data
    message=query.message
    try:
        if data == 'help':
            await query.message.edit_text(Translation.HELP,reply_markup=InlineKeyboard.HELP)
        elif data == 'about':
            await query.message.edit_text(Translation.ABOUT,reply_markup=InlineKeyboard.ABOUT)
        elif data == 'close':
            client.custom_data['batch']=False
            await query.message.delete()
        elif data == 'start':
            await query.message.edit_text(Translation.START,reply_markup=InlineKeyboard.START)
        elif data== 'batch':
            #SetBatchFlag(query.from_user.id) #Set batch flag in database
            client.custom_data['batch']=True
            await query.message.edit_text(Translation.BATCH,reply_markup=InlineKeyboard.BATCH_CANCEL)
        elif data=='cancel_batch':
            client.custom_data['batch']=False
            await message.delete()
        elif data =='login':
            await query.message.edit_text(Translation.LOGIN,reply_markup=InlineKeyboard.LOGIN)
        elif data=='done':
            await DownloadToServer(client,query.from_user.id)
        elif data=='download':
            await Download(client,message.reply_to_message,message)
        
    except Exception as e:
        log(f'Error occured in callback query {e}')


@Dmsbot.on_message(filters.command(['done'])&filters.private)
async def done(client,message):
    await DownloadToServer(client,message.from_user.id)
