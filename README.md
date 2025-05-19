# Government Document Search Agent

This project implements an AI assistant that uses **OpenAI-compatible models via Ollama** to respond to queries by searching through government documents using a custom tool function.

## 🔧 Features

- Uses Ollama-hosted models (like `llama3`, `mistral`, etc.)
- Integrates a custom tool (`search_documents`) to search keywords in government documents
- Supports OpenAI's ChatCompletion API format with function calling
- Ensures model responses are based on the tool's output, not hallucinations

---

## 🚀 Setup

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   python pipeline/fetch_data.py
   python pipeline/push_to_mysql.py
   ollama run mistral:instruct
   uvicorn main:app --reload
   ```

   

   


