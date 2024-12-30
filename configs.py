import os,time
from dotenv import load_dotenv
load_dotenv()

class Configs(object):
    #Bot configurations
    API_ID=int(os.environ.get("API_ID"))
    API_HASH=os.environ.get("API_HASH")
    BOT_TOKEN=os.environ.get("BOT_TOKEN")
    
    #Dms configurations
    Header = '"OCS-APIRequest: true"'
    UploadPoint = '"https://dms.uom.lk/remote.php/webdav/"'
    SharePoint = '"https://dms.uom.lk/ocs/v2.php/apps/files_sharing/api/v1/shares?format=json"'
    MAX_CONCURRENT_TRANSMISSIONS = 2 # Set the maximum amount of concurrent transmissions (uploads & downloads).
    BOT_UPTIME=time.time()
    DOWNLOAD_PATH='./contains'
