from flask import Flask
from google.cloud import secretmanager_v1
import google_crc32c

app = Flask(__name__)

def get_secret(project="57920515119", location="asia-south1", secret="AWS_ACCESS_KEY", version="1"):
    # Create client for regional Secret Manager
    client = secretmanager_v1.SecretManagerServiceClient(client_options={"api_endpoint": f"secretmanager.{location}.rep.googleapis.com"})
    
    # Access the secret version
    name = f"projects/{project}/locations/{location}/secrets/{secret}/versions/{version}"
    resp = client.access_secret_version(request={"name": name})

    # Verify checksum
    crc = google_crc32c.Checksum()
    crc.update(resp.payload.data)
    if resp.payload.data_crc32c != int(crc.hexdigest(), 16):
        raise ValueError("Data corruption detected")

    return resp.payload.data.decode("UTF-8")  # Return secret value

@app.route("/")
def home():
    # Fetch AWS keys
    access = get_secret(secret="AWS_ACCESS_KEY")
    secret_key = get_secret(secret="AWS_SECRET_KEY")
    return f"<h1>Secrets</h1><p>AWS_ACCESS_KEY: {access}</p><p>AWS_SECRET_KEY: {secret_key}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Run Flask app
