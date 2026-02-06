import { useState } from "react";
import { signup, login } from "../api/auth";
import { useAuth } from "../auth/AuthContext";
import styles from "./Signup.module.css";

export default function Signup({ onSwitch }: { onSwitch: () => void }) {
  const { login: saveToken } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    await signup(email, password, firstName, lastName);
    const res = await login(email, password);
    saveToken(res.access_token);
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Create your account</h2>
        <p className={styles.subtitle}>Save resumes and manage them in one place.</p>
      </div>

      <form className={styles.form} onSubmit={handleSubmit}>
        <input
          placeholder="First name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
        />

        <input
          placeholder="Last name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
        />

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
          <button type="submit">Create Account</button>
        </div>
      </form>

      <p className={styles.switchText}>
        Already have an account?{" "}
        <button type="button" className={styles.linkButton} onClick={onSwitch}>
          Sign in
        </button>
      </p>
    </div>
  );
}
