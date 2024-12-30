import os,time
from dotenv import load_dotenv
load_dotenv()

class Configs(object):
    #Bot configurations
    API_ID=int(os.environ.get("API_ID"))
    API_HASH=os.environ.get("API_HASH")
    BOT_TOKEN=os.environ.get("BOT_TOKEN")
    
    #Dms configurations
    UserName=os.environ.get("UserName")
    Password=os.environ.get("Password")
    LoginDetail=f'{os.environ.get("UserName")}:{os.environ.get("Password")}'
    Header = '"OCS-APIRequest: true"'
    UploadPoint = '"https://dms.uom.lk/remote.php/webdav/"'
    SharePoint = '"https://dms.uom.lk/ocs/v2.php/apps/files_sharing/api/v1/shares?format=json"'
    MAX_CONCURRENT_TRANSMISSIONS = 2 # Set the maximum amount of concurrent transmissions (uploads & downloads).
    BOT_UPTIME=time.time()
    WEB_SUPPORT = bool(os.environ.get("WEB_SUPPORT", "True"))
    DOWNLOAD_PATH='./contains'
