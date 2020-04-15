import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db
import json
import requests

# Funtion to get ngrok url
def get_ngrok_url():
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]

cred = credentials.Certificate('firebase_config.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': '',
    'databaseURL': ''
})
bucket = storage.bucket()
ref = db.reference('ml_url')
print(ref.get())

ref.set({
 'ml_url': 'get_ngrok_url()'
})

# Upload image on firebase 

#imageBlob = bucket.blob("temp.jpg")
#imageBlob.upload_from_filename(filename="/home/arun/Desktop/sih/workspace/temp.jpg")
