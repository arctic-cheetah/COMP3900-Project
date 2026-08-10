import requests

analytics = "https://vessel-shorts-arrest.ngrok-free.dev"

# Open and read the text file
with open("my.txt", "r", encoding="utf-8") as file:
    file_content = file.read()

payload = {"message": file_content}

# Send the POST request
response = requests.post(analytics, json=payload)

# Verify the response
print(f"Status Code: {response.status_code}")
