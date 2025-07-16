import requests
from dotenv import load_dotenv
import os

# Charger des informations d'environnement depuis le fichier .env
load_dotenv()

# Accéder aux variables
user = os.getenv("GEOCAT_USERNAME")
pwd = os.getenv("GEOCAT_PASSWORD")
api_url = os.getenv("GEOCAT_URL")

# Affichage des informations
# print(f"api_url: {api_url}")
# print(f"username: {user}")
# print(f"pwd: {pwd}")

session = requests.Session()
session.cookies.clear()

# Stockage des informations d'authentification dans la session
session.auth = (user, pwd)

# Envoi d'une requête GET pour récupérer le token XSRF
try:
    response = session.get(
        api_url + '/me',
        headers={"Accept": "application/json"}
    )
    # print(f"Generated URL: {api_url + '/me'}")  # Affiche l'URL générée
    if response.ok:
        print("Request successful.")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
except requests.exceptions.SSLError as e:
    print("SSL Error:", e)
except requests.exceptions.RequestException as e:
    print("Request Error:", e)

# Copie du token XSRF dans les cookies de la session
token = session.cookies.get("XSRF-TOKEN")
if token:
    print("XSRF-TOKEN:", token)
else:
    print("XSRF-TOKEN not found in cookies.")
