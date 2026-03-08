import flask as f
import src.back.api.sendingFile as sendingFile
import json
import os
from werkzeug.utils import secure_filename

app = f.Flask(
    __name__,
    template_folder="main",
    static_folder="main"
)

uploadFolder = os.path.join(app.instance_path, 'uploads')

if not os.path.exists(uploadFolder):
    os.makedirs(uploadFolder)

app.config['uploadFolder'] = uploadFolder

@app.route("/")
def index():
    return f.render_template("index.html")

@app.route("/popup/<path:filename>")
def popup(filename):
    return f.send_from_directory("main/popup", filename)

@app.route("/api/send/<provider>", methods=["POST"])
def sendFile(provider):
    try:
        if 'file' not in f.request.files:
            return f.jsonify({"error": "No file part in the request"}), 400
        
        uploadedFile = f.request.files['file']
        
        if uploadedFile.filename == '':
            return f.jsonify({"error": "No selected file"}), 400
        
        if uploadedFile:
            filename = secure_filename(uploadedFile.filename)
            tempFilePath = os.path.join(app.config['uploadFolder'], filename)
            
            uploadedFile.save(tempFilePath)
            duration = f.request.form.get('duration')
            result = sendingFile.send(provider, tempFilePath, duration)
            
            try:
                os.remove(tempFilePath)
            except OSError as e:
                app.logger.warning(f"Error removing temporary file {tempFilePath}: {e}")

            if isinstance(result, str) and ("Error:" in result or "Failed:" in result or "Server Error:" in result):
                return f.jsonify({"error": result}), 500
            else:
                return result, 200
        else:
            return f.jsonify({"error": "File upload failed"}), 500

    except Exception as e:
        app.logger.error(f"Error in sendFile endpoint: {e}")
        
        if 'tempFilePath' in locals() and os.path.exists(tempFilePath):
            try:
                os.remove(tempFilePath)
            except OSError as rm_e:
                app.logger.warning(f"Error removing temporary file {tempFilePath} after exception: {rm_e}")
        
        return f.jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

def startWeb():
    if not os.path.exists(uploadFolder):
        os.makedirs(uploadFolder)
    app.run(debug=True)
