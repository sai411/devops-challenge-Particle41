# app/main.py
from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    # current time in ISO 8601 format with timezone
    tz = pytz.timezone(os.getenv("APP_TIMEZONE", "UTC"))
    timestamp = datetime.now(tz).isoformat()
    # get requestor IP (X-Forwarded-For fallback)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return jsonify(timestamp=timestamp, ip=ip)

if __name__ == '__main__':
    # dev only as we are exposing 0.0.0.0
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
