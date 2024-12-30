from configs import Configs
from pyrogram import Client as Dmsbot
from pyrogram.types import CallbackQuery,ForceReply
from pyrogram import filters
from helper.logprint import log
from translation import Translation,InlineKeyboard
from helper.progress import data_convert
import asyncio
import subprocess
import xml.etree.ElementTree as ET
from plugins.download import Download 

#Dmsbot.custom_data['LoginDetail']=Configs.LoginDetail

@Dmsbot.on_callback_query(filters.regex('dmslogin'))
async def login_query(client,query):
    message=query.message
    try:
        await message.reply(Translation.LOGIN_CALL,reply_markup=ForceReply(True,'<USERNAME> <PASSWORD>'))
        await message.delete()
    except Exception as e:
        log(e)

#Force reply filter
async def force_reply_filter(_,client,message):
    if message.reply_to_message.reply_markup and isinstance(message.reply_to_message.reply_markup,ForceReply):
        return True
    else:
        return False
    
@Dmsbot.on_message(filters.private&filters.reply&filters.create(force_reply_filter))
async def login_register(client,message):
    reply_message=message.reply_to_message
    login=message.text
    await asyncio.sleep(2)
    await message.delete()
    log(f'{login} Trying to login')
    try:
        username=login.split()[0]
        password=login.split()[1]
        client.custom_data['LoginDetail']=f'"{username}:{password}"' #Store the login details

    except IndexError:
        await reply_message.reply(Translation.LOGIN_ERROR,reply_markup=ForceReply(True,'<USERNAME> <PASSWORD>'))
        await reply_message.delete()
        
    try:
        result=check_login(client.custom_data.get('LoginDetail'))

        download_flag=client.custom_data.get('downlaod_flag') #Check if download flag is set or not to download the file

        if result and download_flag: #If download flag is set then download the file
            client.custom_data['quota_available']=result #Set the quota available
            SentMessage=await reply_message.reply(Translation.LOGIN_SUCCESS) #Send the login success message
            await reply_message.delete() #Delete the login message
            Message=client.custom_data.get('file_message') #Get the message to download the file
            client.custom_data['download_flag']=False #Reset the download flag
            await Download(client,Message,SentMessage) #call the function to Download the file

        elif result: #If download flag is not set then just login
            await reply_message.reply(Translation.LOGIN_SUCCESS,reply_markup=InlineKeyboard.LOGIN_FINISH)
            client.custom_data['quota_available']=result

        else: #If login failed
            await reply_message.reply(Translation.LOGIN_FAILED,reply_markup=InlineKeyboard.LOGIN_FINISH)
        await reply_message.delete()

    except Exception as e:
        log(e)

#Check login function 
def check_login(LoginDetail):
    try:
        # Define curl command
        uploadPoint = Configs.UploadPoint
        curl_command = f"curl -u {LoginDetail} -X PROPFIND {uploadPoint}"
        
        # Run the curl command
        process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return_code = process.wait()

        # Log errors if any
        if return_code != 0:
            print(f"Error: Curl command failed with return code {return_code}")
            stderr_output = process.stderr.read()
            print(stderr_output)
            return False
        else:
            output = process.stdout.read()
            
        # Log and parse response
        try:
            namespaces = {"d": "DAV:"}  # Define namespace
            root = ET.fromstring(output)
            quota_available = root.find(".//d:quota-available-bytes", namespaces).text
            quota_used = root.find(".//d:quota-used-bytes", namespaces).text
            log(f"Quota Available: {data_convert(int(quota_available))}, Quota Used: {data_convert(int(quota_used))}")
            return quota_available
        except ET.ParseError as e:
            print(f"XML Parsing Error: {e}")
            print(output)  # Log raw response for debugging
            return False


    except Exception as e:
        print(e,'   : in check login')
        return False