import requests
from dotenv import load_dotenv
import os

# Charger des informations d'environnement depuis le fichier .env
load_dotenv()

def authenticate():
    # Accéder aux variables
    user = os.getenv("GEOCAT_USERNAME")
    pwd = os.getenv("GEOCAT_PASSWORD")
    api_url = os.getenv("GEOCAT_URL")

    # Créer une session
    session = requests.Session()
    session.cookies.clear()

    # Stocker les informations d'authentification dans la session
    session.auth = (user, pwd)

    # Envoi d'une requête GET pour récupérer le token XSRF
    try:
        response = session.get(
            api_url + '/me',
            headers={"Accept": "application/json"}
        )
        if response.ok:
            print("Request successful.")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response content:", response.text)
            raise ValueError("Authentication failed.")
    except requests.exceptions.SSLError as e:
        print("SSL Error:", e)
        raise ValueError("SSL Error occurred.")
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
        raise ValueError("Request Error occurred.")

    # Copie du token XSRF dans les cookies de la session
    token = session.cookies.get("XSRF-TOKEN")
    if token:
        print("XSRF-TOKEN:", token)
        session.headers.update({'X-XSRF-TOKEN': token})
        return session, api_url
    else:
        print("XSRF-TOKEN not found in cookies.")
        raise ValueError("XSRF-TOKEN not found.")
