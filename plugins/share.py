from configs import Configs
import subprocess
from helper.logprint import log


async def shareFile(client,fileName):
    SharePoint=Configs.SharePoint
    LoginDetail=client.custom_data.get('LoginDetail')
    curl_command = f'''curl -u username:password -X POST https://webdav.server.url/ocs/v2.php/apps/files_sharing/api/v1/shares \
        -d "path=/path/to/uploaded/file.txt" \
        -d "shareType=3" \
        -d "permissions=1"'
        '''
    process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return_code = process.wait()
    if return_code == 0:
        
        stdout_output = process.stdout.read()
        log(f'Url - {stdout_output}')
        return stdout_output
    else:
        stderr_output = process.stderr.read()
        log(stderr_output)
        return False
    