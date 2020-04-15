import requests

url = 'http://be14272a.ngrok.io'
r = requests.post(url,json={'file_path':'https://upload.wikimedia.org/wikipedia/commons/2/2b/Ruby-LowCompression-Tiny.jpg'})

print(r.json())
