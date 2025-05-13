from flask import Flask, render_template_string, url_for
import json

app = Flask(__name__)

def safe_json_load(filepath):
    """Load only the first valid JSON object, ignoring any trailing data."""
    with open(filepath, "r") as f:
        content = f.read()
        decoder = json.JSONDecoder()
        data, _ = decoder.raw_decode(content)
        return data

@app.route('/')
def homepage():
    logo_path = url_for('static', filename='ramboll_logo.png')
    doc_path_pdf = url_for('static', filename='DNV-ST-0145.pdf')
    sections = [
        {"title": "Section 1 General", "link": "/section/1"},
        {"title": "Section 2 Formal Safety Assessment", "link": "/section/2"},
        {"title": "Section 10 Construction", "link": "/section/10"}
    ]
    html_content = """
    <html>
    <head>
        <title>DNV 0145 Requirements</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }}
            .container {{ width: 80%; margin: auto; overflow: hidden; }}
            header {{ background: #fff; color: #333; padding: 10px 0; border-bottom: #333 solid 1px; }}
            header img {{ width: 150px; float: left; }}
            header h1 {{ text-align: right; float: right; margin: 0; padding-top: 15px; padding-right: 15px; }}
            .section {{ font-size: 1.5em; margin: 1em; color: #0066cc; }}
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <img src="{}" alt="Ramboll Logo">
                <h1>DNV 0145 Requirements</h1>
            </div>
        </header>
        <div class="container">
            <h1>Homepage</h1>
            <div class="section">
                <a href="{}">Download DNV-ST-0145 PDF</a>
            </div>
    """.format(logo_path, doc_path_pdf)

    for section in sections:
        html_content += '<div class="section"><a href="{}">{}</a></div>'.format(section["link"], section["title"])

    html_content += """
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)


@app.route('/section/<section_id>')
def show_section(section_id):
    data = safe_json_load('requirements.json')
    section_data = [section for section in data['DNV0145']['chapters'] if section['chapterTitle'].startswith(f"Section {section_id}")]

    if not section_data:
        return "Section not found", 404

    section = section_data[0]
    logo_path = url_for('static', filename='ramboll_logo.png')
    html_content = """
    <html>
    <head>
        <title>{}</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }}
            .container {{ width: 80%; margin: auto; overflow: hidden; }}
            header {{ background: #fff; color: #333; padding: 10px 0; border-bottom: #333 solid 1px; }}
            header img {{ width: 150px; float: left; }}
            header h1 {{ text-align: right; float: right; margin: 0; padding-top: 15px; padding-right: 15px; }}
            .content {{ padding: 10px; background-color: #fff; border: 1px solid #ddd; margin-bottom: 1em; }}
            .subchapter-title, .title {{ cursor: pointer; color: #0066cc; text-decoration: underline; }}
            h1 {{ color: #333; }}
            h3 {{ color: #0066cc; }}
            ul {{ list-style-type: square; margin-left: 20px; }}
        </style>
        <script>
            function toggleContent(contentId) {{
                var content = document.getElementById(contentId);
                if (content.style.display === 'none') {{
                    content.style.display = 'block';
                }} else {{
                    content.style.display = 'none';
                }}
            }}
        </script>
    </head>
    <body>
        <header>
            <div class="container">
                <img src="{}" alt="Ramboll Logo">
                <h1>DNV 0145 Requirements</h1>
            </div>
        </header>
        <div class="container">
            <h1>{}</h1>
    """.format(section['chapterTitle'], logo_path, section['chapterTitle'])

    for subchapter in section['subchapters']:
        subchapter_id = subchapter['subchapterTitle'].replace(' ', '_')
        html_content += '<div class="subchapter-title" onclick="toggleContent(\'{}\')">{}</div>'.format(subchapter_id, subchapter['subchapterTitle'])
        html_content += '<div class="content" id="{}" style="display:none;">'.format(subchapter_id)
        if 'content' in subchapter:
            html_content += '<p>{}</p>'.format(subchapter['content'])
        if 'requirements' in subchapter:
            html_content += '<h3>Requirements:</h3><ul>'
            for req in subchapter['requirements']:
                html_content += '<li>{}</li>'.format(req)
            html_content += '</ul>'
        html_content += '</div>'

    html_content += '<div class="title" onclick="toggleContent(\'checklist\')">Checklist</div>'
    html_content += '<div class="content" id="checklist" style="display:none;"><h3>Checklist:</h3><ul>'
    for item in section['checklist']:
        html_content += '<li>{}</li>'.format(item)
    html_content += '</ul></div>'
    html_content += '</body></html>'

    return render_template_string(html_content)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
