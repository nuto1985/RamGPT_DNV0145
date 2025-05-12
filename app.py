from flask import Flask, render_template_string
import json

app = Flask(__name__)

@app.route('/')
def homepage():
    html_content = """
    <html><head>
    <title>DNV 0145 Requirements</title>
    <style>
        .section { font-size: 1.5em; margin: 1em 0; }
        .subchapter-content { display: none; padding-left: 2em; }
        .subchapter-title { cursor: pointer; color: blue; text-decoration: underline; }
    </style>
    <script>
        function toggleSubchapter(sectionId) {
            var content = document.getElementById(sectionId);
            if (content.style.display === 'none') {
                content.style.display = 'block';
            } else {
                content.style.display = 'none';
            }
        }
    </script>
    </head>
    <body>
    <h1>DNV 0145 Requirements</h1>
    <div class="section"><a href="/section/10">Section 10 Construction</a></div>
    </body></html>
    """
    return render_template_string(html_content)

@app.route('/section/<section_id>')
def show_section(section_id):
    if section_id != "10":
        return "Section not found", 404

    with open('requirements.json') as f:
        data = json.load(f)
    
    section = data['DNV0145']['chapters'][0]  # Since we only have Section 10
    html_content = """
    <html><head>
    <title>{}</title>
    <style>
        .subchapter-content {{ display: none; padding-left: 2em; }}
        .subchapter-title {{ cursor: pointer; color: blue; text-decoration: underline; }}
    </style>
    <script>
        function toggleSubchapter(subchapterId) {{
            var content = document.getElementById(subchapterId);
            if (content.style.display === 'none') {{
                content.style.display = 'block';
            }} else {{
                content.style.display = 'none';
            }}
        }}
    </script>
    </head><body>
    <h1>{}</h1>
    """.format(section['chapterTitle'], section['chapterTitle'])

    for subchapter in section['subchapters']:
        subchapter_id = subchapter['subchapterTitle'].replace(' ', '_')
        html_content += '<div class="subchapter-title" onclick="toggleSubchapter(\'{}\')">{}</div>'.format(subchapter_id, subchapter['subchapterTitle'])
        html_content += '<div class="subchapter-content" id="{}">'.format(subchapter_id)
        if 'content' in subchapter:
            html_content += '<p>{}</p>'.format(subchapter['content'])
        if 'requirements' in subchapter:
            html_content += '<h3>Requirements:</h3><ul>'
            for req in subchapter['requirements']:
                html_content += '<li>{}</li>'.format(req)
            html_content += '</ul>'
        html_content += '</div>'
    
    html_content += '<h3>Checklist:</h3><ul>'
    for item in section['checklist']:
        html_content += '<li>{}</li>'.format(item)
    html_content += '</ul></body></html>'

    return render_template_string(html_content)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
