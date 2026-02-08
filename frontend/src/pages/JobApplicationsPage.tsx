import { useEffect, useState } from "react";
import {
  fetchJobApplications,
  deleteJobApplication,
  createJobApplication,
  updateJobApplicationStatus,
  updateJobApplicationResume,
  updateJobApplicationDescription,
  fetchAtsScore,
} from "../api/jobApplications";
import type { JobApplication } from "../api/jobApplications";
import type { ApplicationStatus } from "../api/jobApplications";
import type { AtsScoreResult } from "../api/jobApplications";
import { listResumes } from "../api/resumes";
import { useAuth } from "../auth/AuthContext";
import AtsScorePanel from "../components/AtsScorePanel";
import styles from "./JobApplicationsPage.module.css";

export default function JobApplicationsPage() {
  const { token } = useAuth();
  const [apps, setApps] = useState<JobApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [resumes, setResumes] = useState<{ id: string }[]>([]);
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [status, setStatus] = useState<ApplicationStatus>("saved");
  const [editingDescriptionId, setEditingDescriptionId] = useState<
    string | null
  >(null);
  const [descriptionDraft, setDescriptionDraft] = useState("");
  const [atsOpenId, setAtsOpenId] = useState<string | null>(null);
  const [atsData, setAtsData] = useState<AtsScoreResult | null>(null);

  useEffect(() => {
    if (!token) return;

    fetchJobApplications(token)
      .then(setApps)
      .catch(() => setError("Failed to load job applications"))
      .finally(() => setLoading(false));
  }, [token]);

  useEffect(() => {
    if (!token) return;
    listResumes(token).then(setResumes).catch(() => {});
  }, [token]);

  async function handleDelete(id: string) {
    if (!token) return;
    await deleteJobApplication(token, id);
    setApps((prev) => prev.filter((a) => a.id !== id));
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;

    const newApp = await createJobApplication(token, {
      company,
      role,
      status,
    });

    setApps((prev) => [newApp, ...prev]);
    setCompany("");
    setRole("");
    setStatus("saved");
  }

  if (loading) return <p>Loading applications…</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className={styles.container}>
      <h2>Job Applications</h2>

      <form onSubmit={handleCreate} className={styles.form}>
        <input
          placeholder="Company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          required
        />

        <input
          placeholder="Role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          required
        />

        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as ApplicationStatus)}
        >
          <option value="saved">Saved</option>
          <option value="applied">Applied</option>
          <option value="oa">OA</option>
          <option value="interview">Interview</option>
          <option value="rejected">Rejected</option>
        </select>

        <button type="submit">Add</button>
      </form>

      {apps.length === 0 ? (
        <p>No applications yet.</p>
      ) : (
        <ul className={styles.list}>
          {apps.map((app) => (
            <li key={app.id} className={styles.card}>
              <div className={styles.cardContent}>
                <div className={styles.cardLeft}>
                  <strong>{app.company}</strong>
                  <div>{app.role}</div>
                  <select
                    className={styles.status}
                    value={app.status}
                    onChange={async (e) => {
                      if (!token) return;

                      const newStatus = e.target.value as ApplicationStatus;

                      const updated = await updateJobApplicationStatus(
                        token,
                        app.id,
                        newStatus
                      );

                      setApps((prev) =>
                        prev.map((a) => (a.id === app.id ? updated : a))
                      );
                    }}
                  >
                    <option value="saved">Saved</option>
                    <option value="applied">Applied</option>
                    <option value="oa">OA</option>
                    <option value="interview">Interview</option>
                    <option value="rejected">Rejected</option>
                  </select>
                  <select
                    className={styles.resumeSelect}
                    value={app.resume_id ?? ""}
                    onChange={async (e) => {
                      if (!token) return;

                      const value = e.target.value || null;

                      const updated = await updateJobApplicationResume(
                        token,
                        app.id,
                        value
                      );

                      setApps((prev) =>
                        prev.map((a) => (a.id === app.id ? updated : a))
                      );
                    }}
                  >
                    <option value="">No resume attached</option>
                    {resumes.map((resume) => (
                      <option key={resume.id} value={resume.id}>
                        Resume {resume.id.slice(0, 6)}
                      </option>
                    ))}
                  </select>
                </div>
                <div className={styles.cardRight}>
                  <div className={styles.cardActions}>
                    <button
                      className={styles.link}
                      onClick={() => {
                        setEditingDescriptionId(app.id);
                        setDescriptionDraft(app.job_description ?? "");
                      }}
                      type="button"
                    >
                      {app.job_description ? "View / Edit JD" : "Add JD"}
                    </button>
                    <button
                      className={styles.link}
                      onClick={async () => {
                        if (!token) return;

                        if (atsOpenId === app.id) {
                          setAtsOpenId(null);
                          return;
                        }

                        const result = await fetchAtsScore(token, app.id);
                        setAtsData(result);
                        setAtsOpenId(app.id);
                      }}
                      type="button"
                    >
                      View ATS Analysis
                    </button>
                  </div>
                  <button
                    onClick={() => handleDelete(app.id)}
                    className={styles.delete}
                    type="button"
                  >
                    Delete
                  </button>
                </div>
              </div>
              {editingDescriptionId === app.id && (
                <div className={styles.descriptionEditor}>
                  <textarea
                    rows={8}
                    placeholder="Paste job description here..."
                    value={descriptionDraft}
                    onChange={(e) => setDescriptionDraft(e.target.value)}
                  />

                  <div className={styles.editorActions}>
                    <button
                      onClick={async () => {
                        if (!token) return;

                        const updated =
                          await updateJobApplicationDescription(
                            token,
                            app.id,
                            descriptionDraft.trim() || null
                          );

                        setApps((prev) =>
                          prev.map((a) =>
                            a.id === app.id ? updated : a
                          )
                        );

                        setEditingDescriptionId(null);
                      }}
                      type="button"
                    >
                      Save
                    </button>

                    <button
                      className={styles.secondary}
                      onClick={() => setEditingDescriptionId(null)}
                      type="button"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
              {atsOpenId === app.id && atsData && (
                <AtsScorePanel data={atsData} />
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
