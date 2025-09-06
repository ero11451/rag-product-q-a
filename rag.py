from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from werkzeug.utils import secure_filename
from agent import agentExecutor


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