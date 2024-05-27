import boto3
from flask import Flask
from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
import requests
import os

application = app = Flask(__name__)

xray_recorder.configure(service='My Flask Web Application')
XRayMiddleware(app, xray_recorder)
patch_all()

@app.route('/http-call')
def callHTTP():
    requests.get("https://aws.amazon.com")
    return "Test!"

@app.route('/aws-sdk')
def callAWSSDK():
    client = boto3.client('s3')
    client.list_buckets()
    return 'work!'

@app.route('/')
def default():
    return "healthcheck"

if __name__ == "__main__":
    address = os.environ.get('LISTEN_ADDRESS')
    if address is None:
        host = '0.0.0.0'
        port = '5000'
    else:
        host, port = address.split(":")
    app.run(host=host, port=int(port), debug=True)
