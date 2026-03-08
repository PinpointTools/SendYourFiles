import flask as f
import os
import api.sendingFile as sendingFile
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(__file__)

app = f.Flask(
    __name__,
    template_folder="front",
    static_folder="front"
)

isVercel = os.getenv("VERCEL") == "1"
uploadRoot = "/tmp" if isVercel else os.path.join(BASE_DIR, "..", "instance")
uploadFolder = os.path.join(uploadRoot, "uploads")
os.makedirs(uploadFolder, exist_ok=True)

app.config["uploadFolder"] = uploadFolder

@app.route("/")
def index():
    return f.render_template("index.html")

@app.route("/popup/<path:filename>")
def popup(filename):
    return f.send_from_directory(os.path.join(BASE_DIR, "front", "popup"), filename)

@app.route("/api/send/<provider>", methods=["POST"])
def sendFile(provider):
    try:
        if "file" not in f.request.files:
            return f.jsonify({"error": "No file part in the request"}), 400

        uploadedFile = f.request.files["file"]

        if uploadedFile.filename == "":
            return f.jsonify({"error": "No selected file"}), 400

        if uploadedFile:
            filename = secure_filename(uploadedFile.filename)
            tempFilePath = os.path.join(app.config["uploadFolder"], filename)

            uploadedFile.save(tempFilePath)
            duration = f.request.form.get("duration")
            result = sendingFile.send(provider, tempFilePath, duration)

            try:
                os.remove(tempFilePath)
            except OSError as e:
                app.logger.warning(f"Error removing temporary file {tempFilePath}: {e}")

            if isinstance(result, str) and ("Error:" in result or "Failed:" in result or "Server Error:" in result):
                return f.jsonify({"error": result}), 500
            return result, 200

        return f.jsonify({"error": "File upload failed"}), 500

    except Exception as e:
        app.logger.error(f"Error in sendFile endpoint: {e}")

        if "tempFilePath" in locals() and os.path.exists(tempFilePath):
            try:
                os.remove(tempFilePath)
            except OSError as rm_e:
                app.logger.warning(f"Error removing temporary file {tempFilePath} after exception: {rm_e}")

        return f.jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

@app.route("/SendYourFiles.ico")
def faviconICO():
    return f.send_from_directory(os.path.join(BASE_DIR, "public"), "SendYourFiles.ico", mimetype="image/x-icon")

@app.route("/SendYourFiles.png")
def faviconPNG():
    return f.send_from_directory(os.path.join(BASE_DIR, "public"), "SendYourFiles.png", mimetype="image/png")

if __name__ == "__main__":
    os.makedirs(uploadFolder, exist_ok=True)
    app.run(debug=True)
