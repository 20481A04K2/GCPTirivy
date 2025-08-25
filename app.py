from flask import Flask
from google.cloud import secretmanager_v1
import google_crc32c

app = Flask(__name__)

def access_regional_secret_version(
    project_id: str = "57920515119",
    location_id: str = "asia-south1",
    secret_id: str = "AWS_ACCESS_KEY",
    version_id: str = "1",
) -> str:
    """
    Access the payload for the given secret version from Regional Secret Manager.
    """

    # Regional endpoint
    api_endpoint = f"secretmanager.{location_id}.rep.googleapis.com"

    # Create the Secret Manager client with regional endpoint
    client = secretmanager_v1.SecretManagerServiceClient(
        client_options={"api_endpoint": api_endpoint},
    )

    # Build the resource name of the secret version
    name = f"projects/{project_id}/locations/{location_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version
    response = client.access_secret_version(request={"name": name})

    # Verify payload checksum
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        raise ValueError("Data corruption detected.")

    # Decode and return payload
    return response.payload.data.decode("UTF-8")


@app.route("/")
def home():
    # Fetch AWS keys from regional Secret Manager
    aws_access = access_regional_secret_version(
        project_id="57920515119",
        location_id="asia-south1",
        secret_id="AWS_ACCESS_KEY",
        version_id="1"
    )

    aws_secret = access_regional_secret_version(
        project_id="57920515119",
        location_id="asia-south1",
        secret_id="AWS_SECRET_KEY",
        version_id="1"
    )

    return f"""
    <h1>Secrets from Regional Secret Manager</h1>
    <p><b>AWS_ACCESS_KEY:</b> {aws_access}</p>
    <p><b>AWS_SECRET_KEY:</b> {aws_secret}</p>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
