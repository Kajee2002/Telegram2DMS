

import os
import zipfile
#from plugins import 
from pyrogram import Client,filters
from translation import Translation
from plugins.download import BatchDownload
from helper.logprint import log
from configs import Configs
from plugins.share import shareFile
from plugins.upload import uploadToDms
from helper.others import get_file_size


async def zip_huge_files(source_dir, output_zip,client):
    sent_message=client.send_message(Translation.ZIP_INIT)
    """
    Zips a large number of files from a source directory into a single ZIP file.

    Args:
        source_dir (str): Path to the directory containing files to be zipped.
        output_zip (str): Path for the output ZIP file.
    """
    try:
        with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to the zip, maintaining directory structure
                    arcname = os.path.relpath(file_path, start=source_dir)
                    zipf.write(file_path, arcname=arcname)
                    print(f"Added {file_path} as {arcname}")
        print(f"All files in {source_dir} have been zipped into {output_zip}")
    except Exception as e:
        print('Error occured while zipping files \n \t \t',e)
        return
    finally:
        await upload_zip(client,sent_message,file_path,output_zip)


@Client.on_message(filters.command(['zip']))
async def zip_command(client,message):
    if len(message.command)<2:
        sent_message=await message.reply_text(Translation.ZIP_USAGE)
        return
    zip_name=message.command[1]
    if zip_name.endswith('.zip'):
        zip_name=zip_name
    else:
        zip_name=zip_name+'.zip'
    client.custom_data['zip_name']=zip_name
    client.custom_data['zip_flag']=True
    await message.reply(Translation.ZIP_CALL,quote=True)



async def upload_zip(client,sent_message,download_path,zip_name):
    try:
        LoginDetail=client.custom_data.get('LoginDetail')
        UploadPoint=Configs.UploadPoint
        file_size=0
        await uploadToDms(client=client,file_size=file_size,LoginDetail=LoginDetail,fileName=download_path,sent_message=sent_message,UploadPoint=UploadPoint)
    except Exception as e:
        log(e)

    #Remove file from system
    try:os.remove(download_path)
    except Exception as r:log(f'Could not remove {zip_name} : {r}')


    #Get file Url from DMS
    try:
        result = await shareFile(zip_name,LoginDetail)
        await client.sent_message(Translation.SHARE_FILE.format(result))
        return result if result else None
    except Exception as e:
        log(e)