import requests

url="https://nominatim.openstreetmap.org/reverse?format=json&lat=32.9228316&lon=-96.4111491"

headers = {
    'User-Agent': 'Testing Application (www.example.com)',
}
response = requests.get(url, headers=headers)   

print(response.status_code)
response_data = response.json()
print(response_data)