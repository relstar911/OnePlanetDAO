"use client";

import { useEffect, useState } from "react";
import {
  Vote,
  AlertTriangle,
  BarChart3,
  Activity,
  Users,
  Globe,
  TrendingUp,
  ShieldAlert,
} from "lucide-react";
import { api } from "@/lib/api";
import type { KPI, Alert, AnomalyLog, Proposal, Vote as VoteType } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  color = "cyan",
}: {
  icon: React.ElementType;
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}) {
  const colors: Record<string, string> = {
    cyan: "text-cyan-400 bg-cyan-500/10",
    amber: "text-amber-400 bg-amber-500/10",
    violet: "text-violet-400 bg-violet-500/10",
    green: "text-green-400 bg-green-500/10",
  };
  return (
    <div className="glass rounded-xl p-5">
      <div className="flex items-center gap-3 mb-3">
        <div className={`rounded-lg p-2 ${colors[color]}`}>
          <Icon className="h-4 w-4" />
        </div>
        <span className="text-sm text-zinc-400">{label}</span>
      </div>
      <div className="text-2xl font-bold">{value}</div>
      {sub && <div className="mt-1 text-xs text-zinc-500">{sub}</div>}
    </div>
  );
}

function SeverityBadge({ severity }: { severity: string }) {
  const colors: Record<string, string> = {
    low: "bg-green-500/10 text-green-400",
    medium: "bg-amber-500/10 text-amber-400",
    high: "bg-red-500/10 text-red-400",
  };
  return (
    <span
      className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
        colors[severity] || colors.low
      }`}
    >
      {severity}
    </span>
  );
}

export default function DashboardPage() {
  const { isLoggedIn } = useAuth();
  const [votes, setVotes] = useState<VoteType[]>([]);
  const [kpis, setKPIs] = useState<KPI[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyLog[]>([]);
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [loading, setLoading] = useState(true);
  const [backendStatus, setBackendStatus] = useState<string>("checking...");

  useEffect(() => {
    async function load() {
      try {
        const health = await api.healthCheck();
        setBackendStatus(health.status);
      } catch {
        setBackendStatus("offline");
      }

      try {
        const [v, k, al, an, pr] = await Promise.allSettled([
          api.getVotes(),
          api.getKPIs(),
          api.getAlerts(),
          api.getAnomalies(),
          api.getProposals(),
        ]);
        if (v.status === "fulfilled") setVotes(v.value);
        if (k.status === "fulfilled") setKPIs(k.value);
        if (al.status === "fulfilled") setAlerts(al.value);
        if (an.status === "fulfilled") setAnomalies(an.value);
        if (pr.status === "fulfilled") setProposals(pr.value);
      } catch {
        // partial data is fine
      }
      setLoading(false);
    }
    load();
  }, []);

  const [seeding, setSeeding] = useState(false);

  const handleSeed = async () => {
    setSeeding(true);
    try {
      await api.seedDemoData();
      // Reload data
      const [v, k, al, an] = await Promise.allSettled([
        api.getVotes(),
        api.getKPIs(),
        api.getAlerts(),
        api.getAnomalies(),
      ]);
      if (v.status === "fulfilled") setVotes(v.value);
      if (k.status === "fulfilled") setKPIs(k.value);
      if (al.status === "fulfilled") setAlerts(al.value);
      if (an.status === "fulfilled") setAnomalies(an.value);
    } catch {
      // ignore
    }
    setSeeding(false);
  };

  if (loading) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <div className="text-zinc-500 animate-pulse">Loading dashboard...</div>
      </div>
    );
  }

  const isEmpty = votes.length === 0 && kpis.length === 0 && alerts.length === 0 && anomalies.length === 0;
  const collusionAlerts = alerts.filter((a) => a.collusion_flag).length;
  const unresolvedAnomalies = anomalies.filter((a) => !a.resolved).length;
  const avgParticipation =
    kpis.length > 0
      ? (kpis.reduce((s, k) => s + k.participation_rate, 0) / kpis.length).toFixed(1)
      : "N/A";

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="mt-1 text-sm text-zinc-400">
            Real-time overview of governance, fairness, and system health.
          </p>
        </div>
        {isEmpty && (
          <button
            onClick={handleSeed}
            disabled={seeding}
            className="rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-black transition hover:bg-cyan-400 disabled:opacity-50"
          >
            {seeding ? "Seeding..." : "Load Demo Data"}
          </button>
        )}
      </div>

      {/* Empty state */}
      {isEmpty && !seeding && (
        <div className="glass rounded-xl p-8 text-center">
          <Globe className="mx-auto h-12 w-12 text-zinc-600 mb-4" />
          <h3 className="text-lg font-semibold text-zinc-300">No data yet</h3>
          <p className="mt-2 text-sm text-zinc-500 max-w-md mx-auto">
            The dashboard is empty because no governance activity has occurred yet.
            Click &ldquo;Load Demo Data&rdquo; above to populate with sample votes, KPIs, alerts, and anomalies &mdash;
            or log in and start voting!
          </p>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          icon={Vote}
          label="Total Votes"
          value={votes.length}
          sub={`${new Set(votes.map((v) => v.user_id)).size} unique voters`}
          color="cyan"
        />
        <StatCard
          icon={TrendingUp}
          label="Avg Participation"
          value={avgParticipation === "N/A" ? avgParticipation : `${avgParticipation}%`}
          sub={`${kpis.length} regions tracked`}
          color="green"
        />
        <StatCard
          icon={AlertTriangle}
          label="Collusion Alerts"
          value={collusionAlerts}
          sub={`${alerts.length} total alerts`}
          color="amber"
        />
        <StatCard
          icon={ShieldAlert}
          label="Open Anomalies"
          value={unresolvedAnomalies}
          sub={`${anomalies.length} total detected`}
          color="violet"
        />
      </div>

      {/* Backend Status */}
      <div className="glass rounded-xl p-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Activity className="h-5 w-5 text-zinc-400" />
            <span className="font-medium">System Status</span>
          </div>
          <div className="flex items-center gap-2">
            <div
              className={`h-2 w-2 rounded-full ${
                backendStatus === "running" ? "bg-green-400" : "bg-red-400"
              }`}
            />
            <span className="text-sm text-zinc-400">
              Backend: {backendStatus}
            </span>
            <span className="text-sm text-zinc-500 ml-4">
              Auth: {isLoggedIn ? "Authenticated" : "Not logged in"}
            </span>
          </div>
        </div>
      </div>

      {/* Active Proposals */}
      {proposals.length > 0 && (
        <div className="glass rounded-xl p-5">
          <h2 className="mb-4 flex items-center gap-2 font-semibold">
            <BarChart3 className="h-4 w-4 text-cyan-400" />
            Active Proposals ({proposals.length})
          </h2>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {proposals.map((p) => {
              const proposalVotes = votes.filter((v) => v.proposal_id === p.proposal_id);
              return (
                <div
                  key={p.proposal_id}
                  className="rounded-lg bg-white/2 p-4 space-y-2"
                >
                  <div className="font-medium text-sm text-zinc-200">{p.title}</div>
                  {p.description && (
                    <p className="text-xs text-zinc-500 line-clamp-2">{p.description}</p>
                  )}
                  <div className="flex items-center gap-3 text-xs text-zinc-400">
                    <span>{proposalVotes.length} votes</span>
                    <span>{new Set(proposalVotes.map((v) => v.user_id)).size} voters</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Votes */}
        <div className="glass rounded-xl p-5">
          <h2 className="mb-4 flex items-center gap-2 font-semibold">
            <Vote className="h-4 w-4 text-cyan-400" />
            Recent Votes
          </h2>
          {votes.length === 0 ? (
            <p className="text-sm text-zinc-500">No votes recorded yet.</p>
          ) : (
            <div className="space-y-2">
              {votes.slice(-5).reverse().map((v) => (
                <div
                  key={v.id}
                  className="flex items-center justify-between rounded-lg bg-white/2 px-3 py-2 text-sm"
                >
                  <div className="flex items-center gap-2">
                    <Users className="h-3 w-3 text-zinc-500" />
                    <span className="text-zinc-300">{v.user_id}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-zinc-500">Proposal {v.proposal_id}</span>
                    <span className="text-xs text-cyan-400">
                      [{Object.entries(v.vote_weights).map(([k, val]) => `${k}:${val}`).join(", ")}]
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Anomalies */}
        <div className="glass rounded-xl p-5">
          <h2 className="mb-4 flex items-center gap-2 font-semibold">
            <ShieldAlert className="h-4 w-4 text-violet-400" />
            Recent Anomalies
          </h2>
          {anomalies.length === 0 ? (
            <p className="text-sm text-zinc-500">No anomalies detected.</p>
          ) : (
            <div className="space-y-2">
              {anomalies.slice(-5).reverse().map((a) => (
                <div
                  key={a.id}
                  className="flex items-center justify-between rounded-lg bg-white/2 px-3 py-2 text-sm"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-zinc-300">{a.type}</span>
                    <SeverityBadge severity={a.severity} />
                  </div>
                  <span className="text-xs text-zinc-500 max-w-[200px] truncate">
                    {a.description}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* KPIs by Region */}
        <div className="glass rounded-xl p-5">
          <h2 className="mb-4 flex items-center gap-2 font-semibold">
            <BarChart3 className="h-4 w-4 text-green-400" />
            Regional KPIs
          </h2>
          {kpis.length === 0 ? (
            <p className="text-sm text-zinc-500">No KPI data available.</p>
          ) : (
            <div className="space-y-2">
              {kpis.slice(-5).reverse().map((k) => (
                <div
                  key={k.id}
                  className="flex items-center justify-between rounded-lg bg-white/2 px-3 py-2 text-sm"
                >
                  <div className="flex items-center gap-2">
                    <Globe className="h-3 w-3 text-zinc-500" />
                    <span className="text-zinc-300">{k.region}</span>
                  </div>
                  <div className="flex gap-4 text-xs text-zinc-500">
                    <span>
                      Participation:{" "}
                      <span className="text-green-400">{k.participation_rate}%</span>
                    </span>
                    <span>
                      Trust:{" "}
                      <span className="text-cyan-400">{k.trust_index}</span>
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Fairness Alerts */}
        <div className="glass rounded-xl p-5">
          <h2 className="mb-4 flex items-center gap-2 font-semibold">
            <AlertTriangle className="h-4 w-4 text-amber-400" />
            Fairness Alerts
          </h2>
          {alerts.length === 0 ? (
            <p className="text-sm text-zinc-500">No alerts triggered.</p>
          ) : (
            <div className="space-y-2">
              {alerts.slice(-5).reverse().map((a) => (
                <div
                  key={a.id}
                  className="flex items-center justify-between rounded-lg bg-white/2 px-3 py-2 text-sm"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-zinc-300">Epoch {a.epoch}</span>
                    {a.collusion_flag && (
                      <span className="rounded-full bg-red-500/10 px-2 py-0.5 text-xs text-red-400">
                        Collusion
                      </span>
                    )}
                  </div>
                  <div className="flex gap-4 text-xs text-zinc-500">
                    <span>
                      MSI: <span className="text-amber-400">{a.msi.toFixed(2)}</span>
                    </span>
                    <span>
                      VEI: <span className="text-amber-400">{a.vei.toFixed(2)}</span>
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
