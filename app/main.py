from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from refactoring import refactor_and_document
from conversion import convert_ipynb_to_py, convert_py_to_ipynb

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(),"uploads") 
app.config["DOWNLOAD_FOLDER"] = os.path.join(os.getcwd(),"downloads")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/refactor", methods=["POST"])
def refactor():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    upload_file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    download_file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], "refactored_" + filename)
    file.save(upload_file_path)

    # Call the refactor_ipynb function
    refactor_ipynb(upload_file_path, download_file_path)

    # Get the refactored .ipynb file name
    refactored_ipynb_filename = os.path.basename(download_file_path)

    return jsonify({"refactored_ipynb": refactored_ipynb_filename})

@app.route("/download/<string:filename>")
def download(filename):
    #return filename
    return send_from_directory(
        app.config["DOWNLOAD_FOLDER"], 
        "refactored_"+filename, 
        as_attachment=True
    )


def refactor_ipynb(upload_file_path, download_file_path):
    # Convert .ipynb to .py
    py_file_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp.py")
    convert_ipynb_to_py(upload_file_path, py_file_path)
    # Refactor the .py file
    refactored_py_file_path = refactor_and_document(py_file_path, OPENAI_API_KEY)

    # Convert the refactored .py file back to .ipynb
    refactored_ipynb_file_path = convert_py_to_ipynb(py_file_path, download_file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)