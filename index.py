from flask import Flask, send_from_directory, render_template
from flask import redirect, url_for
from livereload import Server
import os
import sys
from markdown import Markdown
from markdown.extensions.wikilinks import WikiLinkExtension

app = Flask(__name__, template_folder="templates", static_url_path="/static")
app.debug = True

# Set the directory to serve
md = Markdown(extensions=["extra", WikiLinkExtension(base_url="/note/")])

NOTE_DIRECTORY = None

def get_file_names():
    files_with_md = [f for f in os.listdir(NOTE_DIRECTORY) if f.endswith('.md')]
    files_without_md = [os.path.splitext(f)[0] for f in files_with_md]
    return files_without_md


@app.route('/')
def index():
    files = get_file_names()
    return render_template('index.html', files=files)

@app.route('/note/<filename>.md')
def redirect_link_with_extension(filename):
    return redirect(url_for('serve_file', filename=filename))

@app.route('/note/<filename>/')
def redirect_wikilinks(filename):
    """
    wikilinks generates the url from [[file-2]] to http://127.0.0.1:5000/note/file-2/
    - the last `/` is extra
    """
    return redirect(url_for('serve_file', filename=filename))

@app.route('/note/<filename>')
def serve_file(filename):
    files = get_file_names()
    file_path = os.path.join(NOTE_DIRECTORY, f"{filename}.md")
    if not os.path.exists(file_path):
        return "File not found", 404
    with open(file_path, 'r') as f:
        content = f.read()
    html_content = md.convert(content)

    # Replace relative image paths to include /notes/images/
    # html_content = html_content.replace('src="', 'src="/static/')
    # this changes the part src=" with src="/notes/ in img tag 

    # print(html_content)
    return render_template('note.html', files=files, filename=filename, content=html_content)


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """
        This function is used because my assets are in my notes directory, 
        not in the app directory
    """
    return send_from_directory(f"{NOTE_DIRECTORY}/assets", filename)

def main():
    if len(sys.argv) < 2:
        print("Usage: python your_script.py <directory>")
        return

    dir_name = sys.argv[1]

    global NOTE_DIRECTORY
    NOTE_DIRECTORY = dir_name

    # app.run(debug=True)
    server = Server(app.wsgi_app)
    server.watch('templates/', delay=1) # Watch the whole project
    server.watch('static/', delay=1)
    server.watch('notes/')
    server.serve()


if __name__ == '__main__':
    main()
