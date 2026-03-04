import os
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Load embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load vector DB
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# LLM
llm = OllamaLLM(model="llama3")

while True:
    query = input("\nAsk a question (type exit to stop): ")

    if query.lower() == "exit":
        break

    docs = retriever.invoke(query)

    context = ""
    for i, doc in enumerate(docs):
        print(f"\nSource {i+1}:")
        print(doc.page_content[:200])
        context += doc.page_content + "\n\n"

    prompt = f"""
    You are an assistant answering questions from a company wiki.

    Rules:
    - Answer only using the provided context
    - If the answer is missing, say "Not found in documentation"
    - Do not make up information

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    print("\nAnswer:\n", response)