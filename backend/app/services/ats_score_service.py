from app.models.job_application import JobApplication
from app.services.ats_match_engine import (
    detect_skills,
    extract_resume_sections,
    score_resume_against_jd,
)


def compute_ats_score(app: JobApplication):
    if not app.job_description or not app.resume:
        return None

    jd_skills = detect_skills(app.job_description)
    total_skills = len(jd_skills)
    sections = extract_resume_sections(app.resume.content)

    skills_counts = detect_skills(sections["skills"])
    experience_counts = detect_skills(sections["experience"])
    projects_counts = detect_skills(sections["projects"])

    evidence: dict[str, dict[str, bool | int]] = {}
    strong_matches: list[str] = []
    weak_matches: list[str] = []
    missing_critical: list[str] = []

    for skill in jd_skills:
        in_skills = skill in skills_counts
        in_experience = skill in experience_counts
        in_projects = skill in projects_counts
        count = (
            skills_counts.get(skill, 0)
            + experience_counts.get(skill, 0)
            + projects_counts.get(skill, 0)
        )

        evidence[skill] = {
            "skills": in_skills,
            "experience": in_experience,
            "projects": in_projects,
            "count": count,
        }

        if in_skills and in_experience:
            strong_matches.append(skill)
        elif in_skills or in_experience or in_projects:
            weak_matches.append(skill)
        else:
            missing_critical.append(skill)

    def section_score(section_counts: dict[str, int]) -> float:
        if total_skills == 0:
            return 0.0
        return round(
            (len([s for s in jd_skills if s in section_counts]) / total_skills)
            * 100,
            2,
        )

    return {
        "overall_score": score_resume_against_jd(
            app.job_description,
            app.resume.content,
        ),
        "section_scores": {
            "skills": section_score(skills_counts),
            "experience": section_score(experience_counts),
            "projects": section_score(projects_counts),
        },
        "strong_matches": sorted(strong_matches),
        "weak_matches": sorted(weak_matches),
        "missing_critical": sorted(missing_critical),
        "evidence": evidence,
    }
