from flask import Flask, render_template_string
import json
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    logo_path = os.path.join('static', 'ramboll_logo.png')
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
        .content {{ padding: 10px; background-color: #fff; border: 1px solid #ddd; margin-bottom: 1em; }}
        .subchapter-title {{ cursor: pointer; color: #0066cc; text-decoration: underline; }}
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
            <img src="{0}" alt="Ramboll Logo">
            <h1>DNV 0145 Requirements</h1>
        </div>
    </header>
    <div class="container">
        <h1>Homepage</h1>
        <div class="section">
            <a href="/section/10">Section 10 Construction</a>
        </div>
    </div>
    </body></html>
    """.format(logo_path)
    return render_template_string(html_content)

@app.route('/section/<section_id>')
def show_section(section_id):
    if section_id != "10":
        return "Section not found", 404

    with open('requirements.json') as f:
        data = json.load(f)

    section = data['DNV0145']['chapters'][0]  # Since we only have Section 10
    logo_path = os.path.join('static', 'ramboll_logo.png')
    html_content = """
    <html><head>
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
    </head><body>
    <header>
        <div class="container">
            <img src="{0}" alt="Ramboll Logo">
            <h1>{1}</h1>
        </div>
    </header>
    <div class="container">
    <h1>{}</h1>
    """.format(logo_path, "DNV 0145 Requirements", section['chapterTitle'])

    for subchapter in section['subchapters']:
        subchapter_id = subchapter['subchapterTitle'].replace(' ', '_')
        html_content += '<div class="subchapter-title" onclick="toggleContent(\'{}\')">{}</div>'.format(subchapter_id, subchapter['subchapterTitle'])
        html_content += '<div class="content" id="{}">'.format(subchapter_id)
        if 'content' in subchapter:
            html_content += '<p>{}</p>'.format(subchapter['content'])
        if 'requirements' in subchapter:
            html_content += '<h3>Requirements:</h3><ul>'
            for req in subchapter['requirements']:
                html_content += '<li>{}</li>'.format(req)
            html_content += '</ul>'
        html_content += '</div>'
    
    html_content += '<div class="title" onclick="toggleContent(\'checklist\')">Checklist</div>'
    html_content += '<div class="content" id="checklist"><h3>Checklist:</h3><ul>'
    for item in section['checklist']:
        html_content += '<li>{}</li>'.format(item)
    html_content += '</ul></div>'
    
    html_content += '</body></html>'

    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
