from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
import textwrap

with open("changi_cleaned.txt","r",encoding="utf-8") as f1:
    text1=f1.read()

with open("jewel_cleaned.txt","r",encoding="utf-8") as f2:
    text2=f2.read()

combined_text=text1+"\n"+text2
combined_text=combined_text.replace("\n"," ").replace("  "," ")

text_chunks=textwrap.wrap(combined_text,width=500)

model=SentenceTransformer('all-MiniLM-L6-v2')
embeddings=model.encode(text_chunks,show_progress_bar=True)

with open("embeddings.pkl","wb") as f:
    pickle.dump((text_chunks,embeddings),f)

