import faiss
import numpy as np

DIM = 384  # MiniLM embedding size
index = faiss.IndexFlatIP(DIM)
job_ids = []

def reset_index():
    global index, job_ids
    index = faiss.IndexFlatIP(DIM)
    job_ids = []

def add_vector(vec, job_id):
    v = np.array([vec]).astype("float32")
    faiss.normalize_L2(v)
    index.add(v)
    job_ids.append(job_id)

def search(vec, k=5):
    v = np.array([vec]).astype("float32")
    faiss.normalize_L2(v)
    scores, idxs = index.search(v, k)
    results = []
    for i in idxs[0]:
        if i < len(job_ids):
            results.append(job_ids[i])
    return results
