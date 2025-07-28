#  VectorRAG Chatbot for Changi Airport

A **context-aware AI chatbot** built using **Google Gemini**, **Pinecone**, and **Streamlit**, trained on website content from **Changi Airport** and **Jewel Changi**. It allows users to ask real-time airport-related queries with highly relevant answers.

---

##  How It Works

This app uses a **Retrieval-Augmented Generation (RAG)** architecture:

1. Changi & Jewel websites are scraped and chunked into embeddings using `SentenceTransformer`.
2. Embeddings are stored in **Pinecone** vector DB.
3. User query is encoded and relevant chunks retrieved from Pinecone.
4. Context + query are passed to **Gemini API** to generate accurate, contextual responses.
5. Users interact with the chatbot through a **Streamlit-based UI**.

---

##  Tech Stack

-  **LLM**: Google Gemini 2.5 Flash (`google-genai`)
-  **Vector Store**: Pinecone
-  **Backend**: FastAPI (deployed on Render)
-  **Frontend**: Streamlit (deployed on Streamlit Cloud)
-  **Embeddings**: `sentence-transformers` (MiniLM)
-  **Secrets**: `.env` locally, `st.secrets` on Streamlit

---

##  Features

- Vector-based semantic search over scraped website content
- Chat UI powered by Gemini
- Clean and minimal UX using Streamlit
- Live deployed on both **Render (API)** and **Streamlit (UI)**

## API Documentation

- Base URL :  https://vectorrag.onrender.com
- Endpoint: /query
- Method: POST
- Description: This endpoint receives a user query, searches for the most relevant chunks of text using Pinecone vector similarity, and returns an AI-generated response using Google's Gemini model.
- Response Body : { "question": "What are the check-in procedures at Changi Airport?"}