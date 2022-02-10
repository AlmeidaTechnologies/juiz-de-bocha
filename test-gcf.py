import requests

url = 'https://southamerica-east1-juiz-de-bocha-teste-gcf.cloudfunctions.net/process-image'
filepath = 'datasets/Jogos de bocha/IMG-20220108-WA0016.jpg'

response = requests.post(
    url,
    files={
        'img': open(filepath, 'rb'),
    },
)

print("Response:", response)
print("Response data:", response.text)
