import json

def load_requirements(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

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

def save_html(html, filename):
    with open(filename, 'w') as f:
        f.write(html)

if __name__ == "__main__":
    data = load_requirements('requirements.json')
    html_content = generate_html(data)
    save_html(html_content, 'requirements.html')