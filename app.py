from flask import Flask
from google.cloud import secretmanager_v1
import google_crc32c

app = Flask(__name__)

def access_secret(resource_id: str) -> str:
    """
    Access a secret using its full resource ID.
    Example:
    projects/57920515119/locations/asia-south1/secrets/AWS_ACCESS_KEY/versions/1
    """
    # Use regional endpoint automatically from resource path
    client = secretmanager_v1.SecretManagerServiceClient()

    # Fetch the secret
    response = client.access_secret_version(request={"name": resource_id})

    # Verify CRC32C checksum
    crc32c = google_crc32c.Checksum()
    crc32c.update(response.payload.data)
    if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
        raise ValueError("Secret payload corrupted!")

    return response.payload.data.decode("UTF-8")

@app.route("/")
def home():
    # Full resource IDs for your secrets
    aws_access_id = "projects/57920515119/locations/asia-south1/secrets/AWS_ACCESS_KEY/versions/1"
    aws_secret_id = "projects/57920515119/locations/asia-south1/secrets/AWS_SECRET_KEY/versions/1"

    aws_access = access_secret(aws_access_id)
    aws_secret = access_secret(aws_secret_id)

    return f"""
    <h1>Secrets in Cloud Run (Regional)</h1>
    <p><b>AWS_ACCESS_KEY:</b> {aws_access}</p>
    <p><b>AWS_SECRET_KEY:</b> {aws_secret}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
