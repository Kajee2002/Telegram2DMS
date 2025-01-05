from helper.logprint import log 
from translation import Translation
import time,os



#Progress bar for downloading progress
async def progress(current,total,*args):
    print("I'm Here in progress")
    current_time=time.time()
    client=args[1]
    last_updated_time=client.custom_data.get('last_updated_time',current_time)
    percentage=current*100/total
    prog=f'{round(percentage,2)}%'
    message=args[0]
    current=data_convert(current)
    total=data_convert(total)
    if current_time-last_updated_time>5:
        #log(Translation.PROGRESS.format(prog=prog,total=total,current=current))
        try:await message.edit_text(Translation.PROGRESS.format(prog=prog,total=total,current=current))
        except Exception as e:log(e)
        client.custom_data['last_updated_time']=current_time


#Progress bar for uploading process
async def uploadProgress(percentage,client,message,total):
    prog=f'{round(percentage,2)}%'
    print(percentage,end='\r')
    current=total*percentage
    await progress(current,total,message,client)



#Data convert 
def data_convert(byte):
    if byte >= 1024**3:  # 1 GB or more
        return f'{round(byte / 1024**3, 2)} GB'
    elif byte >= 1024**2:  # 1 MB to less than 1 GB
        return f'{round(byte / 1024**2, 2)} MB'
    elif byte >= 1024:  # 1 KB to less than 1 MB
        return f'{round(byte / 1024, 2)} KB'
    else:  # Less than 1 KB
        return f'{byte} Bytes'
