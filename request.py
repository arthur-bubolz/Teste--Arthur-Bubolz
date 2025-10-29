import requests

url = "http://localhost:8000/articlemaker"

data = {
    "value": 'Saimaa'
}

response = requests.post(url, json=data)

if response.status_code == 200:
    resultado_json = response.json()
    print(resultado_json) 
else:
    print(f"Erro: {response.status_code}")