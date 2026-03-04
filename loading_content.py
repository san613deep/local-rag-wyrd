import os
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

all_text = ""

for root, dirs, files in os.walk("wiki_folder"):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                all_text += f.read() + "\n"
                
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

print("Total text length:", len(all_text))

chunks = splitter.split_text(all_text)
print("Total chunks:", len(chunks))

# Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create vector database
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

vectorstore.persist()

print("✅ Documents embedded and stored in ChromaDB")

# ask questions like" what is wyrd? or why wyrd?"