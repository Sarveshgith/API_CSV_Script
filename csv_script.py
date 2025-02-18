import requests
import csv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def flatten_dict(d, parent_key='', sep='_'):
    """Recursively flattens a nested dictionary into a single-level dictionary."""
    flattened = {}
    for key, value in d.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened.update(flatten_dict(value, new_key, sep=sep))
        elif isinstance(value, list):
            flattened[new_key] = ", ".join(str(item) for item in value)
        else:
            flattened[new_key] = value
    return flattened

print("1. Get Ticket by Event\n2. Get Ticket by User\n")
choice = int(input("Enter your choice: "))

url = input("Enter the URL: ")
if choice == 1:
    event_id = input("Enter the Event ID: ")
    url = f"{url}/{event_id}"

file_name = input("Enter the file name (without extension): ") + ".csv"
sheet_name = input("Enter the Google Sheet name: ")
auth_type = input("Authentication type (None/Basic/Bearer): ").strip().lower()

headers = {'Content-type': 'application/json'}
response = None

if auth_type == 'bearer':
    bearer_token = input("Enter the Bearer Token: ")
    headers['Authorization'] = f'Bearer {bearer_token}'
    response = requests.get(url, headers=headers)

elif auth_type == 'basic':
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    response = requests.get(url, auth=(username, password), headers=headers)

else:
    response = requests.get(url, headers=headers)

if response and response.status_code == 200:
    response_data = response.json()
    
    if 'data' in response_data and isinstance(response_data['data'], list):
        raw_data = response_data['data']
        
        if not raw_data:
            print("No data found.")
        else:
            flattened_data = [flatten_dict(item) for item in raw_data]

            all_keys = sorted({key for item in flattened_data for key in item.keys()})

            with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=all_keys)
                writer.writeheader()
                for item in flattened_data:
                    writer.writerow({key: item.get(key, "") for key in all_keys})

            print("\nExtracted columns:")
            print(", ".join(all_keys))
            print(f"Data successfully saved to {file_name}")

            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            SERVICE_ACCOUNT_FILE = "local-snow-444516-u5-b239abff2ec4.json"
            
            sheet_id = '1AODVxKmEH5bKiB_Sx-9hvRyOxnOhklma1K01puz9RT'

            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()

            sheet.values().update(
                spreadsheetId=sheet_id,
                range='Sheet1!A1', 
                valueInputOption='RAW',
                body={'values': [all_keys]} 
            ).execute()

            values = [[item.get(key, "") for key in all_keys] for item in flattened_data]
            sheet.values().update(
                spreadsheetId=sheet_id,
                range='Sheet1!A2',
                valueInputOption='RAW',
                body={'values': values}  
            ).execute()

            print(f"Data successfully saved to Google Sheet: {sheet_name}")

    else:
        print("Unexpected data format received.")
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response Text:", response.text)