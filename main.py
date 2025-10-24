import sys
# Import both LLM (OllamaLLM) and Embeddings (OllamaEmbeddings) from the dedicated package
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


# --- Configuration ---
# NOTE: Ensure you have pulled these models using 'ollama pull <model_name>'
LLM_MODEL = "mistral" 
EMBEDDING_MODEL = "nomic-embed-text" 

# --- Setup ---
try:
    # 1. Initialize local Ollama services
    print(f"Connecting to Ollama LLM: {LLM_MODEL}...")
    # Using OllamaLLM instead of Ollama as suggested by the error
    llm = OllamaLLM(model=LLM_MODEL)
    
    print(f"Connecting to Ollama Embeddings: {EMBEDDING_MODEL}...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    print("Please ensure the Ollama server is running and models are downloaded.")
    sys.exit(1)


def format_docs(docs):
    """Formats retrieved documents into a single string for the LLM context."""
    return "\n\n".join(doc.page_content for doc in docs)

def run_pdf_agent(pdf_path: str):
    """
    Main function to run the PDF reading agent.
    """
    print(f"\n--- Loading and Processing PDF: {pdf_path} ---")
    
    # 2. Load the PDF file and split it into pages/chunks
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return

    # 3. Create a Vector Store and Retriever (in-memory for simplicity)
    # The retriever finds document chunks most relevant to the user's question.
    print(f"Loaded {len(pages)} pages/chunks.")
    print("Creating in-memory vector store and retriever...")
    vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4}) # Retrieve top 4 chunks

    # 4. Define the Prompt Template
    template = """
    You are an expert PDF document assistant. Use the following pieces of retrieved context 
    to answer the question. If you don't know the answer, just say that you do not have 
    enough information from the document to answer, don't try to make up an answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # 5. Build the RAG Chain
    # This chain orchestrates the RAG process: Question -> Retrieve -> Context -> LLM -> Answer
    rag_chain = (
        {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 6. Start the interactive chat loop
    print("\n--- Agent Ready! Ask a question about the document ---")
    print("Type 'exit' or 'quit' to end the session.")
    
    while True:
        question = input("\nYour Question: ")
        if question.lower() in ["exit", "quit"]:
            break
        
        if not question.strip():
            continue

        print("\nAgent Answer: ", end="", flush=True)
        # Invoke the chain and stream the response
        try:
            for chunk in rag_chain.stream(question):
                print(chunk, end="", flush=True)
            print() # Newline after the stream is complete
        except Exception as e:
            print(f"\nAn error occurred during LLM invocation: {e}")
            print("Check your Ollama server status and model connectivity.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # NOTE: Updated usage message to reflect 'main.py'
        print("Usage: python main.py <path_to_your_pdf_file>")
        sys.exit(1)
        
    pdf_file_path = sys.argv[1]
    run_pdf_agent(pdf_file_path)
