import { apiFetch } from "./client";
import type { Resume, ResumeListItem } from "../types/resume";

export function listResumes(token: string): Promise<ResumeListItem[]> {
  return apiFetch("/resumes", {}, token);
}

export function createResume(
  token: string,
  content: Record<string, any>
): Promise<Resume> {
  return apiFetch(
    "/resumes",
    {
      method: "POST",
      body: JSON.stringify({ content }),
    },
    token
  );
}

export function deleteResume(token: string, resumeId: string) {
  return apiFetch(
    `/resumes/${resumeId}`,
    { method: "DELETE" },
    token
  );
}
