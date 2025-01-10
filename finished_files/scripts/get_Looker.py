# author: dion@wrench.chat
# tagline_required: 1
# update_date: 1/9/2025
# version: 2

Generate script content for a script named 'get_Looker.py'. The script should have the following description: 'Read your Looker instance metadata and write it to JSON'. The objective is 'Back up your Looker instance content and meta data'. The input parameters are 'Looker privleges and credentials'. The output parameters are 'JSON files'. The language is 'python'. The following labels should be included: '#best_practice
#devops
#diagram
#looker
#platform
#script'.

## Description

This script allows you to quickly and easily back up your Looker instance metadata and content by extracting data from various API endpoints and saving it as JSON files.

## Usage

To use this script, you will need to provide your Looker client ID, client secret, and instance URL. You can either hardcode these values in the script or store them in a `.env` file and load them using the `dotenv` library.

Once you have your credentials, simply run the script and it will automatically:

1. Authenticate with the Looker API
2. Fetch data from various API endpoints
3. Save the extracted data as JSON files in the specified directory

## Input Parameters

* Looker client ID
* Looker client secret
* Looker instance URL

## Output Parameters

* JSON files containing Looker instance metadata and content

## Language

Python

## Labels

* #best_practice
* #devops
* #diagram
* #looker
* #platform
* #script

## Script Content

```python
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
client_id = os.getenv('LOOKER_CLIENT_ID')
client_secret = os.getenv('LOOKER_CLIENT_SECRET')
looker_instance = os.getenv('LOOKER_INSTANCE')

# Directories
output_directory = '/path/to/looker_objects'
os.makedirs(output_directory, exist_ok=True)

# Function to get the authentication token
def get_access_token():
    url = f'{looker_instance}/api/4.0/login'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()['access_token']

# Function to fetch data from API and save it to a file
def fetch_and_save_data(endpoint, token, params=None):
    url = f'{looker_instance}/api/4.0{endpoint}'
    headers = {'Authorization': f'token {token}'}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        file_name = os.path.join(output_directory, f'{endpoint.strip("/").replace("/", "_")}.json')
        
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)
        
        return data  # Return the data for parameter extraction

    except requests.exceptions.HTTPError as err:
        # Output only the error messages
        print(f"Error: HTTP error occurred for {url}: {err}")
        return None
    except Exception as err:
        print(f"Error: An unexpected error occurred for {url}: {err}")
        return None

# Main function
def main():
    token = get_access_token()
    
    # Step 1: Retrieve All Project IDs
    projects_data = fetch_and_save_data('/projects', token)
    
    # Loop through each project to perform further operations
    if projects_data:
        for project in projects_data:
            project_id = project['id']
            git_service_name = project.get('git_service_name')
            
            # Fetch Project-Specific Data
            fetch_and_save_data(f'/projects/{project_id}/manifest', token)
            
            # Skip Git-related operations if the project is a Looker app or plugin
            if git_service_name:
                fetch_and_save_data(f'/projects/{project_id}/credentials', token)
                fetch_and_save_data(f'/projects/{project_id}/git_branches', token)
                fetch_and_save_data(f'/projects/{project_id}/active_git_branch', token)
            
            # Skip LookML-related endpoints if not configured
            if project.get('has_lookml_models', False):
                fetch_and_save_data(f'/projects/{project_id}/lookml_models', token)
            
            # Fetch Folder-Specific Data
            folders_data = fetch_and_save_data('/folders', token)
            if folders_data:
                for folder in folders_data:
                    folder_id = folder['id']
                    fetch_and_save_data(f'/folders/{folder_id}/looks', token)
                    fetch_and_save_data(f'/folders/{folder_id}/dashboards', token)
                    
                    # Fetch Dashboards within the Folder
                    dashboards_data = fetch_and_save_data(f'/folders/{folder_id}/dashboards', token)
                    if dashboards_data:
                        for dashboard in dashboards_data:
                            dashboard_id = dashboard['id']
                            fetch_and_save_data(f'/dashboards/{dashboard_id}', token)

if __name__ == '__main__':
    main()
```
# diagram_pk: dmoyl