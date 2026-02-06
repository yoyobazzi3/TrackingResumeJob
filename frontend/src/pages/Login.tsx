import { useState } from "react";
import { login } from "../api/auth";
import { useAuth } from "../auth/AuthContext";
import styles from "./Login.module.css";

export default function Login({ onSwitch }: { onSwitch: () => void }) {
  const { login: saveToken } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const res = await login(email, password);
    saveToken(res.access_token);
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Welcome back</h2>
        <p className={styles.subtitle}>Sign in to manage your resumes.</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <div className={styles.actions}>
          <button type="submit">Login</button>
        </div>
      </form>

      <p className={styles.switchText}>
        New here?{" "}
        <button type="button" className={styles.linkButton} onClick={onSwitch}>
          Create an account
        </button>
      </p>
    </div>
  );
}
