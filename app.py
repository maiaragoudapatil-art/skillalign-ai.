import streamlit as st
from backend.resume_parser import extract_resume_text, extract_skills, extract_experience
from backend.jd_parser import extract_jd_skills, extract_required_experience
from backend.preprocess import clean_text
from backend.matcher import embed_text, batch_similarity, compute_final_score
from backend.llm_feedback import generate_feedback
from backend.db import init_db, add_job, get_all_jobs, log_missing_skills, get_skill_gap_stats

# ---------- INIT ----------
init_db()
st.set_page_config(page_title="SkillAlign AI", layout="wide")
st.title("SkillAlign AI — Resume & Job Matching Platform")

tab1, tab2, tab3 = st.tabs(["👨‍💼 Job Provider", "👨‍🎓 Candidate", "📊 Analytics"])

# ---------------- JOB PROVIDER ----------------
with tab1:
    st.subheader("Post a Job")

    job_title = st.text_input("Job Title")
    jd_text = st.text_area("Job Description")

    if st.button("Add Job"):
        if job_title and jd_text:
            clean_jd = clean_text(jd_text)
            jd_vec = embed_text(clean_jd)
            add_job(job_title, jd_text, jd_vec)
            st.success("Job saved and indexed")
        else:
            st.warning("Please fill all fields")

# ---------------- CANDIDATE ----------------
with tab2:
    st.subheader("Upload Resume")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    jobs = get_all_jobs()

    if resume_file and jobs:
        resume_text = extract_resume_text(resume_file)
        clean_resume = clean_text(resume_text)

        resume_vec = embed_text(clean_resume)
        job_vecs = [j[3] for j in jobs]
        similarities = batch_similarity(resume_vec, job_vecs)

        resume_skills = extract_skills(resume_text)
        resume_exp = extract_experience(resume_text)

        results = []

        for idx, job in enumerate(jobs):
            job_id, title, jd, _ = job
            jd_skills = extract_jd_skills(jd)
            jd_exp = extract_required_experience(jd)

            score = compute_final_score(
                similarities[idx], resume_skills, jd_skills, resume_exp, jd_exp
            )

            results.append((title, score))

            if 60 <= score <= 85:
                missing, feedback = generate_feedback(jd_skills, resume_skills)
                log_missing_skills(missing)

        results.sort(key=lambda x: x[1], reverse=True)

        st.subheader("📊 Ranked Jobs")

        for title, score in results:
            st.markdown(f"### {title}")
            st.progress(int(score))
            st.write(f"Match Score: **{score}%**")

# ---------------- ANALYTICS ----------------
with tab3:
    st.subheader("Top Skill Gaps Across Candidates")

    stats = get_skill_gap_stats()

    if stats:
        for skill, count in stats:
            st.write(f"{skill} — {count} candidates missing")
    else:
        st.info("Upload resumes to generate analytics.")
