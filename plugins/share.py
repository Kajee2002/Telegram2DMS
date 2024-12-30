from configs import Configs
import subprocess
from helper.logprint import log
import requests
import json

def shareFile(FileName, LoginDetail):
    SharePoint = Configs.SharePoint
    Header = Configs.Header
    permissionBody = f'path={FileName}&shareType=3&permissions=1'  # Directly construct permission body

    try:
        # Perform the POST request using requests
        response = requests.post(SharePoint, data=permissionBody, headers=Header, auth=(LoginDetail[0], LoginDetail[1]))

        # Check if the request was successful
        if response.status_code == 200:
            json_response = response.json()  # Parse the JSON response
            share = json_response['ocs']['data']  # Extract the share data

            # Return the share URL if available
            return share.get("url", None)  # Safely return the URL or None
        else:
            log(f"Error: Unable to share the file. Status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        log(f"Request failed: {e}")
        return None
