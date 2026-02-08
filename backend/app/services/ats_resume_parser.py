def extract_resume_sections(resume: dict) -> dict:
    skills = " ".join(resume.get("skills", []))

    experience = " ".join(
        bullet
        for job in resume.get("experience", [])
        for bullet in job.get("bullets", [])
    )

    projects = " ".join(
        project.get("description", "")
        for project in resume.get("projects", [])
    )

    return {
        "skills": skills.lower(),
        "experience": experience.lower(),
        "projects": projects.lower(),
    }
