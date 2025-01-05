from helper.others import get_file_name,get_file_size
from helper.progress import progress
from helper.logprint import log
from translation import Translation,InlineKeyboard 
from helper.database import dataBase,GetBatchFile,AddBatchFile,ClearBatchFile
from configs import Configs
from pyrogram.errors import RPCError,FloodWait
from plugins.upload import uploadToDms
import urllib.parse
import asyncio
import re
from plugins.share import shareFile
import os
from plugins.zip import zip_huge_files


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
            original_file_name=get_file_name(message)
            file_name=re.sub(r'[^\w\-.]','',original_file_name)
            #file_name = urllib.parse.quote(file_name)
            user=message.from_user.id

            zip_flag=client.custom_data.get('zip_flag')
            if zip_flag:
                zip_name=client.custom_data.get('zip_name')
                download_path=Configs.DOWNLOAD_PATH + '/' + str(user) + '/' + zip_name + '/' + file_name
            else:
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
        if not zip_flag:
            try:
                LoginDetail=client.custom_data.get('LoginDetail')
                UploadPoint=Configs.UploadPoint
                file_size=get_file_size(message)
                await uploadToDms(client=client,file_size=file_size,LoginDetail=LoginDetail,fileName=download_path,sent_message=sent_message,UploadPoint=UploadPoint)
            except Exception as e:
                log(e)

            #Remove file from system
            try:os.remove(download_path)
            except Exception as r:log(f'Could not remove {original_file_name} : {r}')


            #Get file Url from DMS
            try:
                result = await shareFile(file_name,LoginDetail)
                await sent_message.reply_text(Translation.SHARE_FILE.format(result))
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
    client.custom_data['BatchUrls']=[]
    client.custom_data['download_flag']='batch'
    
    count=0
    for i in files:
        result=await Download(client,i[0],i[1])
        if result==True:
            break
        elif result:
            count+=1
            client.custom_data['BatchUrls']=client.custom_data.get('BatchUrls')+[result]
    urls=client.custom_data.get('BatchUrls')

    #Clear batch files from database
    ClearBatchFile(user)

    zip_flag=client.custom_data.get('zip_flag')
    output_file=client.custom_data.get('zip_name')
    if zip_flag:
        await zip_huge_files(client,output_file)
    else:
        try:await client.send_message(user,Translation.BATCH_DONE.format(count,urls))
        except:log(f'Batch Done {urls}')