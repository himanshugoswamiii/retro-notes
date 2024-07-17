## How to run the app ?
```sh
python index.py <notes_directory>
```

---

Q : Why do i've to remove `.md` from file-names ?
- Because wiki links don't work with `.md` extension

Dependencies :
- livereload : famous python package with great integration with Django, Flask

*How to use it ?*
```python
# 1.
from livereload import Server


# 2.
# app.run(debug=True)
# Replace the above with

server = Server(app.wsgi_app)
server.watch('.', delay=1) # Watch the whole project
server.serve()
```
