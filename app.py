from flask import Flask, request, jsonify
import base64
import os
import requests

app = Flask(__name__)

HCTI_API_USER_ID = os.environ.get('HCTI_USER_ID')
HCTI_API_KEY = os.environ.get('HCTI_API_KEY')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    html_content = data.get('html')
    
    response = requests.post(
        'https://hcti.io/v1/image',
        auth=(HCTI_API_USER_ID, HCTI_API_KEY),
        json={'html': html_content}
    )
    
    result = response.json()
    return jsonify({"image_url": result.get('url')})

@app.route('/', methods=['GET'])
def health():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
