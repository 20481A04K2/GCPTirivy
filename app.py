from flask import Flask
import os
from google.cloud import secretmanager

app = Flask(__name__)
client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_id, fallback_env):
    """
    Try fetching secret from Secret Manager.
    If it fails, fall back to environment variable.
    """
    try:
        # Format: projects/{project_id}/locations/{region}/secrets/{secret}/versions/latest
        name = f"projects/57920515119/locations/asia-south1/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        # Fall back to env variable if secret not accessible
        return os.getenv(fallback_env, f"Not Found ({e})")

@app.route("/")
def home():
    aws_access = get_secret("AWS_ACCESS_KEY", "AWS_ACCESS_KEY")
    aws_secret = get_secret("AWS_SECRET_KEY", "AWS_SECRET_KEY")

    return f"""
    <h1>Secrets in Cloud Run</h1>
    <p><b>AWS_ACCESS_KEY:</b> {aws_access}</p>
    <p><b>AWS_SECRET_KEY:</b> {aws_secret}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
