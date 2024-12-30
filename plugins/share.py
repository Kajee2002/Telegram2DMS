from configs import Configs
import subprocess
from helper.logprint import log
import json



async def shareFile(FileName,LoginDetail):
    SharePoint=Configs.SharePoint
    Header = Configs.Header
    permissionBody = str('"'+'path='+FileName+'&shareType=3&permissions=1'+'"')
    json_response = f"!curl -u {LoginDetail} -X POST -d {permissionBody} {SharePoint} -H {Header}"
    json_string = ''.join(json_response)
    share = json.loads(json_string)['ocs']['data']
    try:
        return share["url"]
    except:
        return