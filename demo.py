import json
import requests

url = "https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/London"

result = json.loads(requests.get(url).content)

print(result.get("year"))
