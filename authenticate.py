import requests
from dotenv import load_dotenv
import os

# Remove any existing environment variables
os.environ.clear()

# Load environment variables from the .env file
load_dotenv()

def authenticate():
    # Determine the environment
    environment = os.getenv("ENVIRONMENT", "dev")  # Default to "dev" if not set

    # Select the appropriate URL based on the environment
    if environment == "prod":
        api_url = os.getenv("GEOCAT_URL_PROD")
    elif environment == "dev":
        api_url = os.getenv("GEOCAT_URL_DEV")
    else:
        raise ValueError(f"Invalid environment: {environment}. Use 'dev' or 'prod'.")

    # Access credentials
    user = os.getenv("GEOCAT_USERNAME")
    pwd = os.getenv("GEOCAT_PASSWORD")

    # Create a session
    session = requests.Session()
    session.cookies.clear()

    # Store authentication information in the session
    session.auth = (user, pwd)

    # Send a GET request to retrieve the XSRF token
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

    # Copy the XSRF token into the session cookies
    token = session.cookies.get("XSRF-TOKEN")
    if token:
        print("XSRF-TOKEN:", token)
        session.headers.update({'X-XSRF-TOKEN': token})
        return session, api_url
    else:
        print("XSRF-TOKEN not found in cookies.")
        raise ValueError("XSRF-TOKEN not found.")

if __name__ == "__main__":
    try:
        session, api_url = authenticate()
        print("Authentication successful. Session and API URL are ready to use.")
        print("API URL:", f"{api_url}/me")  # Print the URL
    except ValueError as e:
        print("Authentication failed:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)