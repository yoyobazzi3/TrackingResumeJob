import styles from "./AtsScorePanel.module.css";
import type { AtsScoreResult } from "../api/jobApplications";

interface Props {
  data: AtsScoreResult;
}

export default function AtsScorePanel({ data }: Props) {
  return (
    <div className={styles.panel}>
      <h3>ATS Match Score</h3>
      <div className={styles.score}>{data.overall_score}%</div>

      <div className={styles.badges}>
        {data.strong_matches.map((s) => (
          <span key={s} className={styles.strong}>
            {s}
          </span>
        ))}
        {data.weak_matches.map((s) => (
          <span key={s} className={styles.weak}>
            {s}
          </span>
        ))}
        {data.missing_critical.map((s) => (
          <span key={s} className={styles.missing}>
            {s}
          </span>
        ))}
      </div>

      <table className={styles.table}>
        <thead>
          <tr>
            <th>Skill</th>
            <th>Skills</th>
            <th>Experience</th>
            <th>Projects</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data.evidence).map(([skill, ev]) => (
            <tr key={skill}>
              <td>{skill}</td>
              <td>{ev.skills ? "✔" : "—"}</td>
              <td>{ev.experience ? "✔" : "—"}</td>
              <td>{ev.projects ? "✔" : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
