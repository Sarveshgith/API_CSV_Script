import requests
import csv


print("1. Get Ticket by Event\n2.Get Ticket by User\n")
choice = int(input("Enter your choice: "))

if choice == 1:
    url = input("Enter the URL: ")
    event_id = input("Enter the Event ID: ")
    url = f"{url}/{event_id}"
if choice == 2:
    url = input("Enter the URL: ")

file = input("Enter the file name (without extension): ") + ".csv"
choice = input("Authentication type (None/Basic/Bearer): ").lower()

headers = {'Content-type': 'application/json'}

if choice == 'bearer':
    bearer_token = input("Enter the Bearer Token: ")
    headers['Authorization'] = f'Bearer {bearer_token}'
    response = requests.get(url, headers=headers)

elif choice == 'basic':
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    response = requests.get(url, auth=(username, password), headers=headers)

else:
    response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_data = response.json()
    data = response_data['data']
    
    csv_lines = []

    keys = list(data[0].keys())
    for i in range(len(keys)):
        print(f"{i + 1}. {keys[i]}")

    choice = int(input("Enter the column number to sort the data: "))

    headers = list(data[0][keys[choice - 1]].keys())

    csv_lines.append(headers)

    for item in data:
        values = [str(item[keys[choice - 1]].get(hdr, '')) for hdr in headers]
        csv_lines.append(values)

    with open(file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_lines)

    print(f"Data successfully saved to {file}")

else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response Text:", response.text)
