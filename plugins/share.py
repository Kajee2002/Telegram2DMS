from configs import Configs
import subprocess
from helper.logprint import log
import requests
import json

def shareFile(FileName, LoginDetail):
    SharePoint = Configs.SharePoint
    Header = Configs.Header
    permissionBody = f'path={FileName}&shareType=3&permissions=1'  # Correct string formatting

    try:
        # Send the POST request using requests
        response = requests.post(SharePoint, data=permissionBody, headers=Header, auth=(LoginDetail[0], LoginDetail[1]))
        
        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Try parsing the response as JSON
                json_response = response.json()  # This should return a dictionary
                print(json_response)  # Print for debugging

                # Check if 'ocs' and 'data' exist in the response and safely access the URL
                share = json_response.get('ocs', {}).get('data', {})
                
                # Return the share URL if available
                return share.get("url", None)
            except json.JSONDecodeError:
                print(f"Error: Failed to parse JSON response. Raw response: {response.text}")
                return None
        else:
            print(f"Error: Unable to share the file. Status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
