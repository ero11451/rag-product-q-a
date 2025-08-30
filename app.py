import os
from flask import Flask, jsonify, render_template, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from werkzeug.utils import secure_filename

loader = DirectoryLoader("docs", glob="**/*.*", loader_cls=TextLoader)
raw_docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
docs = splitter.split_documents(raw_docs)

# -------- Vector store / retriever --------
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # ensure model is pulled in Ollama testing

# Correct: build Chroma from documents
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="chroma_db"
)


retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

def format_docs(docs_):
    return "\n\n".join(d.page_content for d in docs_)

# -------- Prompt & model --------
prompt = ChatPromptTemplate.from_template(
    """You are a helpful assistant. Use the context to answer the question.
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:"""
)

model = OllamaLLM(model="llama3.1")  # e.g., "llama3.1" or "llama3.1:8b"

# -------- RAG chain: retriever -> prompt -> model -> text --------
chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

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




if __name__ == "__main__":
    app.run(port=5000, debug=True)
