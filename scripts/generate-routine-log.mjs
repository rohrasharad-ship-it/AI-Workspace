#!/usr/bin/env node
/**
 * Generate data/routine-log.json from projects.md, Linear API, and sweep ledger.
 * Usage: LINEAR_API_KEY=... node scripts/generate-routine-log.mjs
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const PROJECTS_MD = path.join(ROOT, "projects.md");
const LEDGER_PATH = path.join(ROOT, "data", "sweep-runs.jsonl");
const OUT_PATH = path.join(ROOT, "data", "routine-log.json");

const ACTIVE_STATES = new Set([
  "Backlog",
  "Todo",
  "To Do",
  "In Progress",
  "In Review",
]);

const BUG_PREFIX = "🐛";

function parseProjects(md) {
  const rows = [];
  for (const line of md.split("\n")) {
    if (!line.startsWith("|") || line.includes("---")) continue;
    const cols = line
      .split("|")
      .map((c) => c.trim())
      .filter(Boolean);
    if (cols.length < 4 || cols[0] === "Project") continue;
    rows.push({ name: cols[0], linearProjectId: cols[3] });
  }
  return rows;
}

function readLedger() {
  if (!fs.existsSync(LEDGER_PATH)) return [];
  return fs
    .readFileSync(LEDGER_PATH, "utf8")
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}

async function linearGraphql(apiKey, query, variables = {}) {
  const res = await fetch("https://api.linear.app/graphql", {
    method: "POST",
    headers: {
      Authorization: apiKey,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });
  if (!res.ok) {
    throw new Error(`Linear API ${res.status}: ${await res.text()}`);
  }
  const json = await res.json();
  if (json.errors?.length) {
    throw new Error(json.errors.map((e) => e.message).join("; "));
  }
  return json.data;
}

async function fetchProjectIssues(apiKey, projectId) {
  const issues = [];
  let cursor = null;
  const query = `query($projectId: ID!, $after: String) {
    issues(
      filter: { project: { id: { eq: $projectId } } }
      first: 100
      after: $after
      orderBy: updatedAt
    ) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id
        title
        createdAt
        state { name type }
      }
    }
  }`;

  do {
    const data = await linearGraphql(apiKey, query, {
      projectId,
      after: cursor,
    });
    const page = data.issues;
    issues.push(...page.nodes);
    cursor = page.pageInfo.hasNextPage ? page.pageInfo.endCursor : null;
  } while (cursor);

  return issues;
}

function isBug(title) {
  return title.startsWith(BUG_PREFIX);
}

function isPending(stateName) {
  return ACTIVE_STATES.has(stateName);
}

function dayKey(iso) {
  return iso.slice(0, 10);
}

function formatSweepDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function buildSweeps(projectName, issues, ledgerEntries) {
  const byDay = new Map();

  for (const entry of ledgerEntries.filter((e) => e.project === projectName)) {
    const key = dayKey(entry.at);
    byDay.set(key, {
      date: formatSweepDate(entry.at),
      filedBugs: entry.filed?.bugs ?? 0,
      filedFeatures: entry.filed?.features ?? 0,
      clean: Boolean(entry.clean),
      openBugs: 0,
      openFeatures: 0,
      sortKey: entry.at,
    });
  }

  for (const issue of issues) {
    const key = dayKey(issue.createdAt);
    if (!byDay.has(key)) {
      byDay.set(key, {
        date: formatSweepDate(issue.createdAt),
        filedBugs: 0,
        filedFeatures: 0,
        clean: false,
        openBugs: 0,
        openFeatures: 0,
        sortKey: issue.createdAt,
      });
    }
    const row = byDay.get(key);
    const bug = isBug(issue.title);
    if (bug) row.filedBugs += 1;
    else row.filedFeatures += 1;
    if (isPending(issue.state.name)) {
      if (bug) row.openBugs += 1;
      else row.openFeatures += 1;
    }
  }

  return [...byDay.values()]
    .sort((a, b) => (a.sortKey < b.sortKey ? 1 : -1))
    .slice(0, 5)
    .map(({ sortKey: _s, ...rest }) => {
      const filed = rest.filedBugs + rest.filedFeatures;
      const open = rest.openBugs + rest.openFeatures;
      if (rest.clean || filed === 0) {
        return { ...rest, clean: true, filed, open: 0 };
      }
      return { ...rest, clean: false, filed, open };
    });
}

function countSweeps30d(ledger, projectName) {
  const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
  return ledger.filter(
    (e) => e.project === projectName && new Date(e.at).getTime() >= cutoff
  ).length;
}

async function main() {
  const apiKey = process.env.LINEAR_API_KEY;
  if (!apiKey) {
    console.error("error: LINEAR_API_KEY is required");
    process.exit(1);
  }

  const projects = parseProjects(fs.readFileSync(PROJECTS_MD, "utf8"));
  const ledger = readLedger();
  const today = new Date().toISOString().slice(0, 10);

  const projectCards = [];
  let totalPending = 0;
  let totalBugs = 0;
  let totalFeatures = 0;
  let createdToday = 0;
  let sweeps30d = 0;

  for (const project of projects) {
    const issues = await fetchProjectIssues(apiKey, project.linearProjectId);
    const pending = issues.filter((i) => isPending(i.state.name));
    const bugs = pending.filter((i) => isBug(i.title));
    const features = pending.filter((i) => !isBug(i.title));
    const todayCreated = pending.filter((i) => dayKey(i.createdAt) === today);

    totalPending += pending.length;
    totalBugs += bugs.length;
    totalFeatures += features.length;
    createdToday += todayCreated.length;
    sweeps30d += countSweeps30d(ledger, project.name);

    const sweeps = buildSweeps(project.name, issues, ledger);
    const pendingTotal = pending.length;

    projectCards.push({
      name: project.name,
      pendingBugs: bugs.length,
      pendingFeatures: features.length,
      pendingTotal,
      quiet: pendingTotal === 0,
      sweeps,
    });
  }

  const bugPct =
    totalPending > 0 ? Math.round((totalBugs / totalPending) * 100) : 0;
  const featPct = totalPending > 0 ? 100 - bugPct : 0;

  const output = {
    generatedAt: new Date().toISOString(),
    global: {
      pending: totalPending,
      createdToday,
      bugs: totalBugs,
      features: totalFeatures,
      bugPercent: bugPct,
      featurePercent: featPct,
      sweeps30d,
      projectCount: projects.length,
    },
    projects: projectCards,
  };

  fs.mkdirSync(path.dirname(OUT_PATH), { recursive: true });
  fs.writeFileSync(OUT_PATH, JSON.stringify(output, null, 2) + "\n");
  console.log(`Wrote ${OUT_PATH} (${projectCards.length} projects)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
