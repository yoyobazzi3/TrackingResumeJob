import { useState } from "react";
import type { Resume, ResumeListItem } from "../types/resume";
import { deleteResume, getResume } from "../api/resumes";
import { useAuth } from "../auth/AuthContext";
import styles from "./ResumeList.module.css";


export default function ResumeList({
  resumes,
  onDeleted,
}: {
  resumes: ResumeListItem[];
  onDeleted: () => void;
}) {
  const { token } = useAuth();
  const [openResume, setOpenResume] = useState<Resume | null>(null);
  const [loadingId, setLoadingId] = useState<string | null>(null);

  async function handleDelete(id: string) {
    if (!token) return;
    await deleteResume(token, id);
    onDeleted();
  }

  async function handleOpen(id: string) {
    if (!token) return;
    setLoadingId(id);
    const resume = await getResume(token, id);
    setOpenResume(resume);
    setLoadingId(null);
  }

  return (
    <div className={styles.container}>
      <div className={styles.headerRow}>
        <h3 className={styles.title}>Your Resumes</h3>
        <span className={styles.count}>{resumes.length}</span>
      </div>
      <ul className={styles.list}>
        {resumes.map((r) => (
          <li key={r.id} className={styles.item}>
            <button
              className={styles.resumeButton}
              onClick={() => handleOpen(r.id)}
              type="button"
            >
              {r.id}
            </button>
            <button
              className={`${styles.button} ${styles.danger}`}
              onClick={() => handleDelete(r.id)}
            >
              Delete
            </button>
            {loadingId === r.id && (
              <span className={styles.loading}>Loading…</span>
            )}
          </li>
        ))}
      </ul>
      {openResume && (
        <div className={styles.modalOverlay}>
          <div className={styles.modal}>
            <div className={styles.modalHeader}>
              <h4>Resume {openResume.id.slice(0, 8)}</h4>
              <button
                className={styles.modalClose}
                onClick={() => setOpenResume(null)}
                type="button"
              >
                Close
              </button>
            </div>
            <pre className={styles.modalBody}>
              {JSON.stringify(openResume.content, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
