import requests
import json
url="https://f6vk14w3u6.execute-api.us-east-2.amazonaws.com/prod/Websites"
website = {"websiteId": "2002"}
   
r = requests.delete(url,data=json.dumps(website))
print(r.json())