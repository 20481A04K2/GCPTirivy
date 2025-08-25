from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    aws_access = os.getenv("AWS_ACCESS_KEY", "Not Found")
    aws_secret = os.getenv("AWS_SECRET_KEY", "Not Found")

    return f"""
    <h1>Secrets in Cloud Run</h1>
    <p><b>AWS_ACCESS_KEY:</b> {aws_access}</p>
    <p><b>AWS_SECRET_KEY:</b> {aws_secret}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
