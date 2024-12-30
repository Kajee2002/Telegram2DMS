from pyrogram import Client as Dmsbot
from pyrogram import filters
from pyrogram.errors import FloodWait
from translation import Translation,InlineKeyboard
from helper.logprint import log
import subprocess,time,re
from helper.progress import progress,uploadProgress 


#Handle the cURL with progress
async def execute_curl_with_progress(curl_command,client,message,file_size):
    
    # Start the curl command in a subprocess with stdout redirected
    process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    try:
        # Initialize variables to store the previous progress
        client.custom_data['last_updated_time']=time.time()
        progress=0
        # Loop through the output of the command
        for line in process.stderr:
            # Extract progress information using regex
            match = re.search(r'(\d+(\.\d+)?)%', line)
            if match:
                progress = float(match.group(1))
                try:
                  await uploadProgress(progress,client,message,file_size )
                  #await message.edit_text(f'Uploading from server to DMS... \n {progress_bar(progress)}')
                except:
                  pass
            else:
                # Skip lines that don't contain progress updates
                continue
        # Wait for the process to finish and get the return code
        return_code = process.wait()
        # Check if the command was successful
        if return_code == 0:
            await message.edit_text("File uploaded to DMS successfully.")
            return True
        else:
            stderr_output = process.stderr.read()
            await message.edit_text("Error occurred during file upload.")
            print(f"Error during upload: {stderr_output.strip()}")
            return False
    except Exception as e:
      await message.edit_text("An error occurred:", e)
      print("\nAn error occurred:", e)
      return False


#Function to Upload file to Dms
async def uploadToDms(client,file_size,LoginDetail,fileName,UploadPoint,sent_message):
     # Construct the curl command with --progress-bar option
  curl_command = f'curl -u {LoginDetail} --progress-bar -T "{fileName}" "{UploadPoint}"'

  # Execute the curl command and show progress
  result= await execute_curl_with_progress(curl_command,client,sent_message,file_size)
  
  log(result)