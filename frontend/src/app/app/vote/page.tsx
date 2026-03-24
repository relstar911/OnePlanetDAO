"use client";

import { useEffect, useState } from "react";
import { Vote, Send, CheckCircle, AlertCircle, Info } from "lucide-react";
import { api } from "@/lib/api";
import type { Vote as VoteType } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function VotingPage() {
  const { isLoggedIn, userId } = useAuth();
  const [votes, setVotes] = useState<VoteType[]>([]);
  const [loading, setLoading] = useState(true);

  // Form state
  const [proposalId, setProposalId] = useState("");
  const [weights, setWeights] = useState("1");
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .getVotes()
      .then(setVotes)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleVote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLoggedIn || !userId) {
      setError("Please log in first.");
      return;
    }
    setError("");
    setSuccess("");
    setSubmitting(true);

    try {
      const voteWeights = weights
        .split(",")
        .map((w) => parseFloat(w.trim()))
        .filter((w) => !isNaN(w));

      if (voteWeights.length === 0) {
        setError("Enter at least one vote weight (e.g. 1,2,3)");
        setSubmitting(false);
        return;
      }

      await api.submitVote({
        user_id: userId,
        proposal_id: proposalId,
        vote_weights: voteWeights,
        proof: "zk-proof-placeholder",
      });

      setSuccess("Vote submitted successfully!");
      setProposalId("");
      setWeights("1");

      const updated = await api.getVotes();
      setVotes(updated);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to submit vote");
    } finally {
      setSubmitting(false);
    }
  };

  // Quadratic cost calculation
  const totalCost = weights
    .split(",")
    .map((w) => parseFloat(w.trim()))
    .filter((w) => !isNaN(w))
    .reduce((sum, w) => sum + w * w, 0);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Quadratic Voting</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Express the strength of your preference. Cost grows quadratically — 1
          vote costs 1 credit, 2 votes cost 4, 3 cost 9.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-5">
        {/* Vote Form */}
        <div className="lg:col-span-2">
          <form onSubmit={handleVote} className="glass rounded-xl p-6 space-y-5">
            <h2 className="flex items-center gap-2 font-semibold">
              <Send className="h-4 w-4 text-cyan-400" />
              Cast Your Vote
            </h2>

            {!isLoggedIn && (
              <div className="flex items-center gap-2 rounded-lg bg-amber-500/10 border border-amber-500/20 px-4 py-3 text-sm text-amber-400">
                <AlertCircle className="h-4 w-4 shrink-0" />
                You need to log in before voting.
              </div>
            )}

            {error && (
              <div className="flex items-center gap-2 rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
                <AlertCircle className="h-4 w-4 shrink-0" />
                {error}
              </div>
            )}

            {success && (
              <div className="flex items-center gap-2 rounded-lg bg-green-500/10 border border-green-500/20 px-4 py-3 text-sm text-green-400">
                <CheckCircle className="h-4 w-4 shrink-0" />
                {success}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1.5">
                Proposal ID
              </label>
              <input
                type="text"
                value={proposalId}
                onChange={(e) => setProposalId(e.target.value)}
                required
                placeholder="e.g. climate-fund-2026"
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-zinc-300 mb-1.5">
                Vote Weights
              </label>
              <input
                type="text"
                value={weights}
                onChange={(e) => setWeights(e.target.value)}
                required
                placeholder="e.g. 1,2,3"
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
              />
              <p className="mt-1.5 text-xs text-zinc-500">
                Comma-separated. Each weight represents your preference strength.
              </p>
            </div>

            {/* Quadratic Cost Display */}
            <div className="flex items-center gap-2 rounded-lg bg-cyan-500/5 border border-cyan-500/10 px-4 py-3 text-sm">
              <Info className="h-4 w-4 text-cyan-400 shrink-0" />
              <span className="text-zinc-400">
                Quadratic cost:{" "}
                <span className="font-bold text-cyan-400">{totalCost}</span>{" "}
                Soul-Credits
              </span>
            </div>

            <button
              type="submit"
              disabled={submitting || !isLoggedIn}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-black transition hover:bg-cyan-400 disabled:opacity-50"
            >
              {submitting ? "Submitting..." : "Submit Vote"}
            </button>
          </form>
        </div>

        {/* Vote History */}
        <div className="lg:col-span-3">
          <div className="glass rounded-xl p-6">
            <h2 className="mb-4 flex items-center gap-2 font-semibold">
              <Vote className="h-4 w-4 text-cyan-400" />
              Vote History
              <span className="ml-auto text-xs font-normal text-zinc-500">
                {votes.length} total
              </span>
            </h2>

            {loading ? (
              <p className="text-sm text-zinc-500 animate-pulse">Loading...</p>
            ) : votes.length === 0 ? (
              <p className="text-sm text-zinc-500">
                No votes yet. Be the first to participate!
              </p>
            ) : (
              <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2">
                {[...votes].reverse().map((v) => (
                  <div
                    key={v.id}
                    className="rounded-lg bg-white/[0.02] px-4 py-3 text-sm"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium text-zinc-300">
                        {v.user_id}
                      </span>
                      <span className="text-xs text-zinc-500">
                        Proposal: {v.proposal_id}
                      </span>
                    </div>
                    <div className="mt-1 flex items-center gap-2">
                      <span className="text-xs text-zinc-500">Weights:</span>
                      {v.vote_weights.map((w, i) => (
                        <span
                          key={i}
                          className="rounded bg-cyan-500/10 px-1.5 py-0.5 text-xs text-cyan-400"
                        >
                          {w}
                        </span>
                      ))}
                      <span className="ml-auto text-xs text-zinc-500">
                        Cost: {v.vote_weights.reduce((s, w) => s + w * w, 0)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
