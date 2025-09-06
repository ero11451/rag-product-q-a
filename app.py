import os
from flask import Flask, jsonify, render_template, request
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from werkzeug.utils import secure_filename
from agent import agentExecutor
from rag import chain

# -------- Flask app --------
app = Flask(__name__)

UPLOAD_FOLDER = './docs'
ALLOWED_EXTENSIONS = {'txt', 'md', 'pdf'}  # adjust as needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' in JSON body"}), 400
    try:
        answer = chain.invoke(question)
        return  jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        f = request.files['file']
        if f.filename == '':
            return "No selected file", 400
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)  # avoid unsafe filenames
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(save_path)
            return f"File uploaded: {filename}", 200
        else:
            return "File type not allowed", 400
    return render_template('upload.html')

@app.route('/agent', methods = ['GET', 'POST'])
def agential():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    if request.method == 'POST':
        try:
            answer = agentExecutor.invoke({"input": question})
            return  jsonify({"answer": answer})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('agent.html')

@app.route('/search', methods = ['GET', 'POST'])
def search():
    data = request.get_json(silent=True) or {}
    question = data.get("question")
    if request.method == 'POST':
        try:
            answer = agentExecutor.invoke({"input": question})
            return  jsonify({"answer": answer})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('search.html')
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)
