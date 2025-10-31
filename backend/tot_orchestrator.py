from sentence_transformers import SentenceTransformer, util#sentenceTransformer converts the text into numerical embeddings(vectors) 
#and util is used for calculating similarity between embeddings
import numpy as np

model= SentenceTransformer("all-MiniLM-L6-v2")
#explanation
#Converts both the question and one candidate answer into embeddings.
#Measures how similar they are using cosine similarity:
#Score is close to 1 → very similar.
#Score near 0 → unrelated.
def score_candidate(candidate_text: str, question: str):
    q_emb= model.encode(question, convert_to_tensor=True)
    c_emb= model.encode(candidate_text, convert_to_tensor=True)
    return float(util.cos_sim(q_emb, c_emb).item())

#explanation to function-Loops over all candidate answers.
#Scores each one using score_candidate().
#Sorts them by score (highest first).
#Picks the best match — the one most semantically related to the question.
def choose_best(candidates, question):
    scored=[]
    for cand in candidates:
        s= score_candidate(cand["text"], question)
        scored.append((s, cand))
    scored.sort(key=lambda x: x[0], reverse=True)
    best= scored[0][1]
    return best, scored

if __name__ == "__main__":
    question = "What is the role of attention in a transformer model?"
    candidates = [
        {"text": "Attention helps the model focus on relevant parts of the input sequence while generating output."},
        {"text": "Transformers use pooling layers to compress text into smaller representations."},
        {"text": "Transformers are mainly used for computer vision tasks only."}
    ]
    best, scored = choose_best(candidates, question)
    print("Best Answer:", best)
    print("\nScores:")
    for s, c in scored:
        print(f"{s:.3f} → {c['text']}")