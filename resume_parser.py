import fitz  # PyMuPDF
import json

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(resume_text):
    skills_db = [
        "python", "java", "c++", "c", "html", "css", "javascript", "sql",
        "django", "flask", "react", "node", "git", "github", "mysql",
        "data analysis", "machine learning", "deep learning", "nlp", "excel"
    ]
    resume_text = resume_text.lower()
    extracted_skills = [skill for skill in skills_db if skill in resume_text]
    return extracted_skills

def match_jobs(skills, job_profiles_file):
    with open(job_profiles_file, 'r') as f:
        job_profiles = json.load(f)

    matched_jobs = []
    for job in job_profiles:
        required = set(job['skills_required'])
        present = set(skills)
        matched = required.intersection(present)
        match_percent = (len(matched) / len(required)) * 100

        matched_jobs.append({
            'title': job['title'],
            'matched_skills': list(matched),
            'match_percent': round(match_percent, 2)
        })

    return matched_jobs

def match_career_fields(skills, job_clusters_file):
    with open(job_clusters_file, 'r') as f:
        job_clusters = json.load(f)

    matched_fields = []
    for cluster in job_clusters:
        required = set(cluster['skills'])
        matched = required.intersection(set(skills))
        score = (len(matched) / len(required)) * 100
        matched_fields.append({
            'field': cluster['field'],
            'suggested_roles': cluster['roles'],
            'match_percent': round(score, 2),
            'matched_skills': list(matched),
            'missing_skills': list(required - matched)
        })

    # Sort by best match
    matched_fields.sort(key=lambda x: x['match_percent'], reverse=True)
    return matched_fields

# -------------------- Testing --------------------
if __name__ == "__main__":
    resume_text = extract_text_from_pdf("ShubhamCV.pdf")
    print("🔍 Extracted Resume Text:\n", resume_text[:500], "\n...")

    skills = extract_skills(resume_text)
    print("\n✅ Extracted Skills:")
    print(skills)

    job_matches = match_jobs(skills, "job_profiles.json")
    print("\n📋 Job Matching Results:")
    for job in job_matches:
        print(f"\n💼 {job['title']}")
        print(f"✅ Matched Skills: {job['matched_skills']}")
        print(f"📊 Match: {job['match_percent']}%")

    # Smart Field Matching
    field_matches = match_career_fields(skills, "job_clusters.json")
    print("\n🌐 Smart Career Field Suggestions:")
    for field in field_matches[:3]:  # Top 3 suggestions
        print(f"\n🏆 Field: {field['field']}")
        print(f"💼 Suggested Roles: {', '.join(field['suggested_roles'])}")
        print(f"✅ Matched Skills: {field['matched_skills']}")
        print(f"📊 Fit Score: {field['match_percent']}%")
        print(f"❌ Missing Skills: {', '.join(field['missing_skills'])}")
