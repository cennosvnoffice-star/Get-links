import requests

CLIENT_ID = "icwnfnjml3m21c2"
CLIENT_SECRET = "j12579um0i2tget"
CODE = "bi45BrlxwhMAAAAAACIAD-UAV2qpA2BQ4X6qSq81Tl4"
REDIRECT_URI = "http://127.0.0.1:5000/"

url = "https://api.dropboxapi.com/oauth2/token"

data = {
    "code": CODE,
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
}

resp = requests.post(url, data=data)
print(resp.json())
