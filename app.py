from flask import Flask, render_template_string, request, jsonify, url_for
import json
import os
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = 'your_openai_api_key'

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
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; }
        .container { width: 80%; margin: auto; overflow: hidden; }
        header { background: #fff; color: #333; padding: 10px 0; border-bottom: #333 solid 1px; }
        header img { width: 150px; float: left; }
        header h1 { text-align: right; float: right; margin: 0; padding-top: 15px; padding-right: 15px; }
        .section { font-size: 1.5em; margin: 1em; color: #0066cc; }
        .content { padding: 10px; background-color: #fff; border: 1px solid #ddd; margin-bottom: 1em; }
        .subchapter-title { cursor: pointer; color: #0066cc; text-decoration: underline; }
        h1 { color: #333; }
        h3 { color: #0066cc; }
        ul { list-style-type: square; margin-left: 20px; }
        .chat-container { margin-top: 20px; }
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

        function sendMessage() {{
            var userMessage = document.getElementById('userInput').value;
            fetch('/chat', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{message: userMessage}})
            }})
            .then(response => response.json())
            .then(data => {{
                var chatBox = document.getElementById('chatBox');
                chatBox.innerHTML += '<b>You:</b> ' + userMessage + '<br><b>Bot:</b> ' + data.reply + '<br><br>';
                document.getElementById('userInput').value = '';
            }});
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
        <h1>Homepage</h1>
        <div class="section">
            <a href="{}">Download DNV-ST-0145 PDF</a>
        </div>
        """.format(logo_path, doc_path_pdf)

    for section in sections:
        html_content += '<div class="section"><a href="{}">{}</a></div>'.format(section["link"], section["title"])

    html_content += """
        <div class="chat-container">
            <h3>Chat with Rambly</h3>
            <div id="chatBox" style="border: 1px solid #ddd; padding: 10px; height: 200px; overflow-y: auto;"></div>
            <input type="text" id="userInput" placeholder="Type your message here" style="width: 80%;">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>
    </body></html>
    """
    return render_template_string(html_content)

@app.route('/section/<section_id>')
def show_section(section_id):
    with open('requirements.json') as f:
        data = json.load(f)
    
    section_data = [section for section in data['DNV0145']['chapters'] if section['chapterTitle'].startswith(f"Section {section_id}")]

    if not section_data:
        return "Section not found", 404

    section = section_data[0]
    logo_path = url_for('static', filename='ramboll_logo.png')
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

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )
    reply = response.choices[0].text.strip()
    return jsonify({'reply': reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
