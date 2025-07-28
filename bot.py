import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from pydantic import BaseModel
import streamlit as st

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API"))
pc=Pinecone(api_key=os.getenv("API_KEY"))

index_name="changiindex"
index=pc.Index(index_name)

model= SentenceTransformer("all-MiniLM-L6-v2")

app=FastAPI()

class Query(BaseModel):
    question:str

def get_response(query,k=3):
    query_vector=model.encode(query).tolist()
    query_response=index.query(vector=query_vector,top_k=k,include_metadata=True)
    context=[match["metadata"]["text"] for match in query_response["matches"]]
    prompt=f"""Answer the following user question based on the following context
            context:{context}
            Question:{query}"""
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a chatbot. You have knowledge about airport sector"
        ),
        contents=prompt
    )
    return response.candidates[0].content.parts[0].text

@app.post("/query")
def api_answer(data:Query):
    answer=get_response(data.question)
    return {"Answer":answer}



