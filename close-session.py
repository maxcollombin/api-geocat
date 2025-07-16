import requests

session = requests.Session()

# Close the session
session.close()
print("Session closed.")