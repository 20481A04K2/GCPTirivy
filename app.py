from flask import Flask
import os
from google.cloud import secretmanager_v1
import google_crc32c

app = Flask(__name__)

def access_regional_secret(project_id, location_id, secret_id, version_id="latest"):
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})

    # Verify CRC32C checksum
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        raise ValueError("Secret payload corrupted!")

    return response.payload.data.decode("UTF-8")

@app.route("/")
def home():
    project_id = "sylvan-hydra-464904-d9"
    location_id = "asia-south1"  # Regional Secret Manager location
    aws_access = access_regional_secret(project_id, location_id, "AWS_ACCESS_KEY")
    aws_secret = access_regional_secret(project_id, location_id, "AWS_SECRET_KEY")

    return f"""
    <h1>Secrets in Cloud Run (Regional)</h1>
    <p><b>AWS_ACCESS_KEY:</b> {aws_access}</p>
    <p><b>AWS_SECRET_KEY:</b> {aws_secret}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
