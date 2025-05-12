from flask import Flask, render_template_string, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('requirements.json') as f:
        data = json.load(f)
    html_content = generate_html(data)
    return render_template_string(html_content)

def generate_html(data):
    html = "<html><body>"
    for chapter in data['DNV0145']['chapters']:
        html += f"<h1>{chapter['chapterTitle']}</h1>"
        for subchapter in chapter['subchapters']:
            html += f"<h2>{subchapter['subchapterTitle']}</h2>"
            html += "<h3>Requirements:</h3><ul>"
            for req in subchapter['requirements']:
                html += f"<li>{req}</li>"
            html += "</ul><h3>Checklist:</h3><ul>"
            for item in subchapter['checklist']:
                html += f"<li>{item}</li>"
            html += "</ul>"
    html += "</body></html>"
    return html

if __name__ == "__main__":
    app.run(debug=True)