import { readFile } from "node:fs/promises";
import path from "node:path";

// This page intentionally remains a Server Component so runtime files stay local.

type SessionOutput = {
  raw_idea: string;
  timestamp: string;
  blueprint: {
    industry: string;
    complexity_tier: "Low" | "Medium" | "High";
    immediate_competitors: string[];
    brutal_premise_flaw: string;
  };
  market_risk: {
    tam_estimate: string;
    sam_estimate: string;
    som_estimate: string;
    risk_score: number;
    success_probability: number;
    market_blockers: string[];
  };
  conclusion_text: string;
};

export const dynamic = "force-dynamic";

async function readSession(): Promise<SessionOutput> {
  const outputPath = path.resolve(process.cwd(), "..", "session_output.json");
  const contents = await readFile(outputPath, "utf8");
  return JSON.parse(contents) as SessionOutput;
}

export default async function Home() {
  const data = await readSession();

  return (
    <main className="page-shell">
      <header className="masthead">
        <div>
          <p className="eyebrow">Startup Validator / Investment Memo</p>
          <h1>Market validation, without the theatre.</h1>
        </div>
        <p className="timestamp">Updated {new Date(data.timestamp).toLocaleString()}</p>
      </header>

      <div className="card-grid">
        <section className="report-card">
          <p className="card-number">01 / Blueprint</p>
          <h2>{data.blueprint.industry}</h2>
          <dl className="definition-list">
            <div>
              <dt>Complexity</dt>
              <dd>{data.blueprint.complexity_tier}</dd>
            </div>
            <div>
              <dt>Immediate competitors</dt>
              <dd>{data.blueprint.immediate_competitors.join(" · ")}</dd>
            </div>
          </dl>
          <div className="critical-note">
            <p className="eyebrow">Premise flaw</p>
            <p>{data.blueprint.brutal_premise_flaw}</p>
          </div>
        </section>

        <section className="report-card">
          <div className="card-heading">
            <div>
              <p className="card-number">02 / Market &amp; Risk</p>
              <h2>Commercial reality</h2>
            </div>
            <div className="viability-badge">
              <strong>{data.market_risk.success_probability}%</strong>
              <span>Market viability</span>
            </div>
          </div>
          <div className="market-figures">
            {[
              ["TAM", data.market_risk.tam_estimate],
              ["SAM", data.market_risk.sam_estimate],
              ["SOM", data.market_risk.som_estimate],
            ].map(([label, value]) => (
              <div key={label}>
                <span>{label}</span>
                <p>{value}</p>
              </div>
            ))}
          </div>
          <p className="risk-score tabular-nums">
            Risk score <strong>{data.market_risk.risk_score}/100</strong>
          </p>
          <ul className="blocker-list">
            {data.market_risk.market_blockers.map((blocker) => (
              <li key={blocker}>{blocker}</li>
            ))}
          </ul>
        </section>

        <section className="report-card report-card-wide">
          <p className="card-number">03 / Validator Report</p>
          <p className="eyebrow">Original idea</p>
          <p className="idea-text">{data.raw_idea}</p>
          <div className="verdict">
            <p className="eyebrow">Incubator verdict</p>
            <blockquote>{data.conclusion_text}</blockquote>
          </div>
          <a className="deck-link" href="/api/pitch-deck" target="_blank">
            Open investor deck <span aria-hidden="true">↗</span>
          </a>
        </section>
      </div>
    </main>
  );
}
