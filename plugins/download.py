from helper.others import get_file_name,get_file_size
from helper.progress import progress
from helper.logprint import log
from translation import Translation,InlineKeyboard 
from helper.database import dataBase,GetBatchFile,AddBatchFile
from configs import Configs
from pyrogram.errors import RPCError,FloodWait
from plugins.upload import uploadToDms
import urllib.parse
import asyncio
from plugins.share import shareFile

async def Download(client,message,sent_message):
    available_dms_storage=client.custom_data.get('quota_available')
    file_size=get_file_size(message)
    if not available_dms_storage:
        client.custom_data['downlaod_flag']=True #Set the download flag to download the file after login
        client.custom_data['file_message']=message #Store the message to download after login
        try:await sent_message.edit_text(Translation.LOGIN_FIRST,reply_markup=InlineKeyboard.LOGIN) #Ask user to login first
        except FloodWait as e:asyncio.sleep(e)
        return True
    
    elif int(available_dms_storage)<int(file_size):
        try:await sent_message.reply(Translation.QUOTA_EXCEDED)
        except FloodWait as e:asyncio.sleep(e)
        return True
    else:
        try:
            await sent_message.edit_text(Translation.DOWNLOADING)
            file_name=get_file_name(message)
            file_name = urllib.parse.quote(file_name)
            user=message.from_user.id
            download_path=Configs.DOWNLOAD_PATH + "/"+str(user)+'/'+file_name
            log(f'File Name : {file_name} Download Initiated...')
            file_path =await message.download(file_name=download_path,progress=progress,progress_args=(sent_message,client,Translation.DOWNLOADING))
            client.custom_data['file_path']=file_path
            client.custom_data['file_name']=file_name
            if file_path:
                try:
                    await sent_message.edit(Translation.DOWNLOADED)
                    log('File downloaded successfully')
                except Exception as e:
                    log(f'Error occured while sending message {e}')
                    pass
        
        except RPCError as e:
            await sent_message.edit(Translation.DOWNLOAD_ERROR)
            log(f'Error occured while downloading file. {e}')
        except ValueError as e:
            await sent_message.edit(Translation.DOWNLOAD_ERROR)
            log(f'Error occured while downloading file. {e}')
        
        #Upload TO DMS CALL
        try:
            LoginDetail=client.custom_data.get('LoginDetail')
            UploadPoint=Configs.UploadPoint
            file_size=get_file_size(message)
            await uploadToDms(client=client,file_size=file_size,LoginDetail=LoginDetail,fileName=download_path,sent_message=sent_message,UploadPoint=UploadPoint)
            
        except Exception as e:
            log(e)

        try:
            result = await shareFile(file_name,LoginDetail,sent_message)
            await sent_message.edit_text(Translation.SHARE_FILE.format(result))
            return result if result else None

        except Exception as e:
            log(e)

async def BatchDownload(client,message):
    sent_message= await message.reply(Translation.BATCH_ADD,reply_markup=InlineKeyboard.BATCH_ADD,reply_to_message_id=message.id)
    AddBatchFile(message.from_user.id,message,sent_message)


#From Done 
async def DownloadToServer(client,user):
    files=GetBatchFile(user)
    #print(files)
    client.custon_data['BatchUrls']=[]
    count=0
    for i in files:
        result=await Download(client,i[0],i[1])
        if result==True:
            break
        elif result:
            count+=1
            client.custom_data['BatchUrls'].append(result)
    urls=client.custom_data.get('BatchUrls')
    try:await client.send_message(user,Translation.BATCH_DONE.format(count,urls))
    except:log(f'Batch Done {urls}')