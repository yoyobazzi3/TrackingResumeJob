import type { ResumeListItem } from "../types/resume";
import { deleteResume } from "../api/resumes";
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

  async function handleDelete(id: string) {
    if (!token) return;
    await deleteResume(token, id);
    onDeleted();
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
            <span className={styles.id}>{r.id}</span>
            <button
              className={`${styles.button} ${styles.danger}`}
              onClick={() => handleDelete(r.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
