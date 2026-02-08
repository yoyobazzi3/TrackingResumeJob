from app.models.job_application import JobApplication
from app.services.ats_match_engine import detect_skills, ats_score
from app.services.ats_resume_parser import extract_resume_sections


def compute_keyword_match(app: JobApplication):
    if not app.job_description or not app.resume:
        return None

    result = ats_score(app.job_description, app.resume.content)
    return {
        "overall_score": result["overall_score"],
        "strong_matches": sorted(result["strong_matches"]),
        "weak_matches": sorted(result["weak_matches"]),
        "missing_critical": sorted(result["missing_critical"]),
        "evidence": result["evidence"],
    }
