import pickle
from pinecone import Pinecone,ServerlessSpec
import os
from dotenv import load_dotenv


load_dotenv()
with open("embeddings.pkl","rb") as f:
    text_chunks,embeddings=pickle.load(f)

pc=Pinecone(api_key=os.getenv("API_KEY"))
environment="us-east-1"
index_name="changiindex"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws",region=environment)
    )

index=pc.Index(index_name)

vectors=[(f"id-{i}",embeddings[i],{"text":text_chunks[i]})
         for i in range(len(embeddings))
]

for i in range(0,len(vectors),100):
    index.upsert(vectors[i:i+100],show_progress=True)
