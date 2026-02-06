import { useState } from "react";
import { createResume } from "../api/resumes";
import { useAuth } from "../auth/AuthContext";
import styles from "./ResumeForm.module.css";

export default function ResumeForm({ onCreated }: { onCreated: () => void }) {
  const [text, setText] = useState("");
  const { token } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;

    await createResume(token, { raw: text });
    setText("");
    onCreated();
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <h3 className={styles.title}>Create Resume</h3>

      <textarea
        className={styles.textarea}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste your resume here..."
      />

      <div className={styles.actions}>
        <button type="submit">Create</button>
      </div>
    </form>
  );
}
