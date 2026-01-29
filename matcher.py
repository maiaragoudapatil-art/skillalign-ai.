from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    return model.encode(text)

def batch_similarity(resume_vec, job_vecs):
    sims = cosine_similarity([resume_vec], job_vecs)[0]
    return sims.tolist()

def compute_final_score(text_sim, resume_skills, jd_skills, resume_exp, jd_exp):
    skill_score = len(set(resume_skills) & set(jd_skills)) / max(len(jd_skills), 1)
    exp_score = min(resume_exp / max(jd_exp, 1), 1)

    final_score = (
        0.6 * text_sim +
        0.25 * skill_score +
        0.15 * exp_score
    )
    return round(final_score * 100, 2)
