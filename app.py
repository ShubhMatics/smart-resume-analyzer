import streamlit as st
import fitz
import re
import json

# ----------- Extract Functions -----------

def extract_text_from_pdf(uploaded_file):
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(text):
    skills_db = [
        "python", "java", "c++", "c", "html", "css", "javascript", "sql",
        "django", "flask", "react", "node", "git", "github", "mysql",
        "data analysis", "machine learning", "deep learning", "nlp", "excel"
    ]
    text = text.lower()
    return [skill for skill in skills_db if skill in text]

def extract_email(text):
    return re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)

def extract_phone(text):
    return re.findall(r"\+91[-\s]?\d{10}|\b\d{10}\b", text)

def extract_name(lines, email):
    for i, line in enumerate(lines):
        if email and email[0] in line:
            for j in range(i-1, -1, -1):
                if lines[j].strip():
                    return lines[j].strip()
    return "Not Found"

def extract_section(lines, keywords):
    return [line.strip() for line in lines if any(word in line.lower() for word in keywords)]

def match_career_fields(skills, clusters_file='job_clusters.json'):
    with open(clusters_file, 'r') as f:
        clusters = json.load(f)
    matches = []
    for cluster in clusters:
        matched = list(set(skills).intersection(set(cluster['skills'])))
        score = (len(matched) / len(cluster['skills'])) * 100
        matches.append({
            "field": cluster['field'],
            "roles": cluster['roles'],
            "match_percent": round(score, 2),
            "matched_skills": matched,
            "missing_skills": list(set(cluster['skills']) - set(matched))
        })
    return sorted(matches, key=lambda x: x['match_percent'], reverse=True)

# ----------- Streamlit UI Starts -----------

st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")
st.title("📄  Resume Analyzer  ")
st.subheader("Upload your resume (PDF) and get career suggestions instantly! it is a project made by shubham ")

uploaded_file = st.file_uploader("📥 Upload your Resume", type=["pdf"])

if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        text = extract_text_from_pdf(uploaded_file)
        lines = text.split("\n")

        email = extract_email(text)
        phone = extract_phone(text)
        name = extract_name(lines, email)
        skills = extract_skills(text)
        education = extract_section(lines, ["education", "diploma", "college", "school", "university"])
        experience = extract_section(lines, ["experience", "intern", "developer", "manager", "worked", "company"])
        matches = match_career_fields(skills)

    st.success("✅ Analysis Complete!")

    st.header("🙋 Candidate Info")
    st.markdown(f"**👤 Name:** {name}")
    st.markdown(f"**📧 Email:** {email[0] if email else 'Not Found'}")
    st.markdown(f"**📱 Phone:** {phone[0] if phone else 'Not Found'}")

    st.header("🧠 Extracted Skills")
    st.markdown(", ".join(skills) if skills else "Not Found")

    st.header("🎓 Education")
    for edu in education:
        st.markdown(f"- {edu}")

    st.header("💼 Experience")
    for exp in experience:
        st.markdown(f"- {exp}")

    st.header("🌐 Career Suggestions")
    for field in matches[:3]:
        st.subheader(f"🏆 {field['field']}")
        st.markdown(f"**💼 Roles:** {', '.join(field['roles'])}")
        st.markdown(f"**✅ Matched Skills:** {', '.join(field['matched_skills'])}")
        st.markdown(f"**❌ Missing Skills:** {', '.join(field['missing_skills'])}")
        st.markdown(f"**📊 Match Score:** {field['match_percent']}%")
        st.markdown("---")
