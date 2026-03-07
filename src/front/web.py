import flask as f

app = f.Flask(
    __name__,
    template_folder="main",
    static_folder="main"
)

@app.route("/")
def index():
    return f.render_template("index.html")

@app.route("/popup/<path:filename>")
def popup(filename):
    return f.send_from_directory("main/popup", filename)

def startWeb():
    app.run(debug=True)