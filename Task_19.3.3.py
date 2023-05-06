import requests

params = {'status': 'pending'}
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
url = 'https://petstore.swagger.io/v2/'

res = requests.get(f'{url}pet/findByStatus', params=params, headers=headers)

print(res.status_code)
print(res.text)

data = {
  "id": 1,
  "category": {
    "id": 2,
    "name": "Max"
  },
  "name": "doggie",
  "photoUrls": [
    "Def"
  ],
  "tags": [
    {
      "id": 3,
      "name": "Lolo"
    }
  ],
  "status": "available"
}
res = requests.post(f'{url}pet', headers=headers, json=data)

print(res.status_code)
print(res.text)

res = requests.delete(f'{url}pet/2')

print(res.status_code)
print(res.json())

data = {
  "id": 4,
  "category": {
    "id": 6,
    "name": "Semm"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}
res = requests.put(f'{url}pet', json=data)

print(res.status_code)
print(res.json())
