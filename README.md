🂡 🂱 🂽 Local Ai Agent 🃁 🃔 🂮
Uno rules, manuals, PDFs... the AI always plays the right card.

# Local PDF RAG Agent Using Ollama + LangChain

Ask questions to any PDF using fully local AI models. This project uses Retrieval-Augmented Generation (RAG) to extract meaningful context from documents and generate accurate answers, all while keeping data private on your machine.

Perfect for rulebooks, manuals, reports… and in this case: Uno game rules!

✅ Features

• Local inference through Ollama
• Uses embeddings to retrieve the most relevant PDF chunks
• Interactive chat interface in the terminal
• Prevents hallucination with context-aware prompting
• Swap AI models easily (Mistral, Llama, etc.)
• Lightweight in-memory vector store

🔧 Tech Stack
Component	Tool
LLM	Mistral via Ollama
Embeddings	nomic-embed-text
Framework	LangChain
Vector Store	DocArray In-Memory Search
Document Loader	PyPDFLoader
Language	Python 3.10+
📦 Prerequisites

Install Python and Ollama:

• Download Ollama: https://ollama.ai/download

• Pull required models:

ollama pull mistral
ollama pull nomic-embed-text

🚀 Installation
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

▶️ How to Run

Start Ollama:

ollama serve


Run the agent:

python main.py sample_docs/uno_rules.pdf


Ask your questions!

Your Question: What is a Wild Draw 4 card?


Exit anytime using:

exit


or

quit

📁 Project Structure
.
├── main.py
├── sample_docs/
│   └── uno_rules.pdf  (optional example)
├── requirements.txt
├── README.md
└── .gitignore

💡 Example Questions

• What is the main objective of Uno?
• When can a Draw 2 card be played?
• What does a Reverse card do?

🛠 Troubleshooting
Issue	Possible Fix
Model fails to load	Check if Ollama is running: ollama serve
PDF not found	Confirm correct file path
Slow first-time response	Model is loading for the first run
🗺 Roadmap

• Support multiple PDFs
• RAG UI using Streamlit
• Chat history memory
• GPU performance optimizations
• Docker support for easy deployment

🤝 Contributions

Open to improvements. PRs welcome!

📜 License

MIT License. Use and modify freely.

🙌 Credits

• LangChain community
• Ollama team
• Uno card game creators (fun guaranteed)
