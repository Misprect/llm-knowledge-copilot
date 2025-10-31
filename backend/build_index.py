import json, os
from pathlib import Path 
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np 

BASE= Path(__file__).parent
DATA_PATH= BASE/"data"/ "genai_knowledge_base.json"
INDEX_PATH= BASE/ "index.faiss"
META_PATH= BASE/ "metadata.npy"

model= SentenceTransformer("all-MiniLM-L6-v2")

print("Loading JSON:", DATA_PATH)
with open(DATA_PATH, "r", encoding="utf-8") as f:
    kb= json.load(f)

#use enterprise_version if possible and there else use educational_version
texts=[]
metas=[]
for item in kb:
    text= item.get("enterprise_version") or item.get("educational_version") or item.get("topic") or ""
    texts.append(text)
    metas.append({"id": item.get("id"), "topic": item.get("topic"), "source": item.get("source")})
print("Encodinng", len(texts), "chunks...")
embs= model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

#normalize then index
faiss.normalize_L2(embs)
d= embs.shape[1]
index= faiss.IndexFlatIP(d)
index.add(embs)

faiss.write_index(index, str(INDEX_PATH))
np.save(META_PATH, np.array(metas, dtype=object))
print("Saved index", INDEX_PATH)
print("Saved metadata", META_PATH)