from collections import defaultdict

from app.services.ats_skills import CANONICAL_SKILLS
from app.services.ats_resume_parser import extract_resume_sections

SECTION_WEIGHTS = {
    "skills": 3.0,
    "experience": 2.0,
    "projects": 1.5,
}


def detect_skills(text: str):
    found = defaultdict(int)
    for skill, variants in CANONICAL_SKILLS.items():
        for variant in variants:
            if variant in text:
                found[skill] += text.count(variant)
    return found


def ats_score(job_description: str, resume: dict):
    jd_text = job_description.lower()
    jd_skills = detect_skills(jd_text)

    sections = extract_resume_sections(resume)
    evidence = {}
    score = 0
    max_score = len(jd_skills) * max(SECTION_WEIGHTS.values())

    for skill in jd_skills:
        evidence[skill] = {
            "skills": False,
            "experience": False,
            "projects": False,
            "count": 0,
        }

        for section, weight in SECTION_WEIGHTS.items():
            detected = detect_skills(sections[section])
            if skill in detected:
                evidence[skill][section] = True
                evidence[skill]["count"] += detected[skill]
                score += weight

    overall = round(score / max_score * 100) if max_score else 0

    strong = [
        key for key, value in evidence.items()
        if value["skills"] and value["experience"]
    ]
    weak = [
        key for key, value in evidence.items()
        if value["skills"] and not value["experience"]
    ]
    missing = [key for key, value in evidence.items() if value["count"] == 0]

    return {
        "overall_score": overall,
        "strong_matches": strong,
        "weak_matches": weak,
        "missing_critical": missing,
        "evidence": evidence,
    }
