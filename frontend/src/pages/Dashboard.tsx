import { useEffect, useState } from "react";
import { listResumes } from "../api/resumes";
import type { ResumeListItem } from "../types/resume";
import ResumeForm from "../components/ResumeForm";
import ResumeList from "../components/ResumeList";
import { useAuth } from "../auth/AuthContext";
import styles from "./Dashboard.module.css";

export default function Dashboard() {
  const [resumes, setResumes] = useState<ResumeListItem[]>([]);
  const { token, logout } = useAuth();

  async function loadResumes() {
    if (!token) return;
    const data = await listResumes(token);
    setResumes(data);
  }

  useEffect(() => {
    loadResumes();
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Resume Dashboard</h1>
        <button onClick={logout}>Logout</button>
      </div>

      <div className={styles.content}>
        <ResumeForm onCreated={loadResumes} />
        <ResumeList resumes={resumes} onDeleted={loadResumes} />
      </div>
    </div>
  );
}
