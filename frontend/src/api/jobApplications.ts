const API_URL = import.meta.env.VITE_API_URL

export type ApplicationStatus =
  | "saved"
  | "applied"
  | "oa"
  | "interview"
  | "rejected";

export interface JobApplication {
  id: string;
  company: string;
  role: string;
  status: ApplicationStatus;
  resume_id?: string | null;
  job_description?: string | null;
  created_at: string;
}

export interface CreateJobApplicationPayload {
  company: string;
  role: string;
  status?: ApplicationStatus;
  resume_id?: string | null;
  job_description?: string | null;
}

function authHeaders(token: string) {
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}

export async function fetchJobApplications(token: string) {
  const res = await fetch(`${API_URL}/job-applications`, {
    headers: authHeaders(token),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch job applications");
  }

  return res.json() as Promise<JobApplication[]>;
}

export async function createJobApplication(
  token: string,
  payload: CreateJobApplicationPayload
) {
  const res = await fetch(`${API_URL}/job-applications`, {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to create job application");
  }

  return res.json() as Promise<JobApplication>;
}

export async function deleteJobApplication(
  token: string,
  id: string
) {
  const res = await fetch(`${API_URL}/job-applications/${id}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });

  if (!res.ok) {
    throw new Error("Failed to delete job application");
  }
}

export async function updateJobApplicationStatus(
  token: string,
  id: string,
  status: ApplicationStatus
) {
  const res = await fetch(`${API_URL}/job-applications/${id}`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify({ status }),
  });

  if (!res.ok) {
    throw new Error("Failed to update status");
  }

  return res.json() as Promise<JobApplication>;
}

export async function updateJobApplicationResume(
  token: string,
  id: string,
  resumeId: string | null
) {
  const res = await fetch(`${API_URL}/job-applications/${id}`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify({ resume_id: resumeId }),
  });

  if (!res.ok) {
    throw new Error("Failed to update resume");
  }

  return res.json() as Promise<JobApplication>;
}

export async function updateJobApplicationDescription(
  token: string,
  id: string,
  description: string | null
) {
  const res = await fetch(`${API_URL}/job-applications/${id}`, {
    method: "PATCH",
    headers: authHeaders(token),
    body: JSON.stringify({ job_description: description }),
  });

  if (!res.ok) {
    throw new Error("Failed to update job description");
  }

  return res.json() as Promise<JobApplication>;
}

export interface KeywordMatchResult {
  overall_score: number;
  strong_matches: string[];
  weak_matches: string[];
  missing_critical: string[];
  evidence: Record<
    string,
    { skills: boolean; experience: boolean; projects: boolean }
  >;
}

export async function fetchKeywordMatch(
  token: string,
  appId: string
) {
  const res = await fetch(
    `${API_URL}/job-applications/${appId}/keyword-match`,
    {
      headers: authHeaders(token),
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch keyword match");
  }

  return res.json() as Promise<KeywordMatchResult>;
}

export interface AtsEvidence {
  skills: boolean;
  experience: boolean;
  projects: boolean;
  count: number;
}

export interface AtsScoreResult {
  overall_score: number;
  strong_matches: string[];
  weak_matches: string[];
  missing_critical: string[];
  evidence: Record<string, AtsEvidence>;
}

export async function fetchAtsScore(
  token: string,
  appId: string
) {
  const res = await fetch(
    `${API_URL}/job-applications/${appId}/ats-score`,
    {
      headers: authHeaders(token),
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch ATS score");
  }

  return res.json() as Promise<AtsScoreResult>;
}
