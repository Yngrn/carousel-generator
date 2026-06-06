from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import base64
import os
import tempfile

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    html_content = data.get('html')
    
    slides_b64 = []
    
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
        f.write(html_content)
        tmp_path = f.name
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        page.goto(f"file://{tmp_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        for slide in page.query_selector_all(".slide"):
            png = slide.screenshot()
            slides_b64.append(base64.b64encode(png).decode())
        browser.close()
    
    os.unlink(tmp_path)
    return jsonify({"slides": slides_b64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
