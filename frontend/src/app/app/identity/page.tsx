"use client";

import { useState } from "react";
import {
  Fingerprint,
  Shield,
  CheckCircle,
  AlertCircle,
  Send,
  UserCheck,
} from "lucide-react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function IdentityPage() {
  const { isLoggedIn, userId } = useAuth();

  // Proof Request form
  const [proofType, setProofType] = useState("onboarding");
  const [signals, setSignals] = useState("signal1");
  const [nullifier, setNullifier] = useState("ext-null-001");
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleProofRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isLoggedIn || !userId) {
      setError("Please log in first.");
      return;
    }
    setError("");
    setSuccess("");
    setSubmitting(true);

    try {
      await api.submitProofRequest({
        user_id: userId,
        proof_type: proofType,
        public_signals: signals.split(",").map((s) => s.trim()),
        external_nullifier: nullifier,
      });
      setSuccess("Proof request submitted successfully!");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to submit proof request");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Identity & Verification</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Prove you are a unique human without revealing who you are.
          Zero-knowledge cryptography protects your privacy.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* How it works */}
        <div className="glass rounded-xl p-6 space-y-4">
          <h2 className="flex items-center gap-2 font-semibold">
            <Shield className="h-4 w-4 text-cyan-400" />
            How Identity Works
          </h2>

          <div className="space-y-3">
            {[
              {
                icon: Fingerprint,
                title: "Proof of Personhood",
                desc: "Submit a zero-knowledge proof that you are a unique human. No personal data is stored or shared.",
              },
              {
                icon: UserCheck,
                title: "One Person, One Vote",
                desc: "Your proof ensures Sybil resistance — no one can create multiple accounts to manipulate votes.",
              },
              {
                icon: Shield,
                title: "Guardian Recovery",
                desc: "Assign trusted guardians who can help you recover your identity if you lose access. No central authority needed.",
              },
            ].map((item) => (
              <div
                key={item.title}
                className="flex gap-3 rounded-lg bg-white/2 p-3"
              >
                <item.icon className="h-5 w-5 text-cyan-400 mt-0.5 shrink-0" />
                <div>
                  <div className="text-sm font-medium">{item.title}</div>
                  <div className="text-xs text-zinc-500 mt-0.5">{item.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Proof Request Form */}
        <form
          onSubmit={handleProofRequest}
          className="glass rounded-xl p-6 space-y-5"
        >
          <h2 className="flex items-center gap-2 font-semibold">
            <Send className="h-4 w-4 text-cyan-400" />
            Submit Proof Request
          </h2>

          {!isLoggedIn && (
            <div className="flex items-center gap-2 rounded-lg bg-amber-500/10 border border-amber-500/20 px-4 py-3 text-sm text-amber-400">
              <AlertCircle className="h-4 w-4 shrink-0" />
              Log in to submit a proof request.
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
              Proof Type
            </label>
            <select
              value={proofType}
              onChange={(e) => setProofType(e.target.value)}
              className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
            >
              <option value="onboarding" className="bg-zinc-900">
                Onboarding (First-time verification)
              </option>
              <option value="recovery" className="bg-zinc-900">
                Recovery (Re-verification)
              </option>
              <option value="voting" className="bg-zinc-900">
                Voting (Per-session proof)
              </option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">
              Public Signals
            </label>
            <input
              type="text"
              value={signals}
              onChange={(e) => setSignals(e.target.value)}
              required
              placeholder="signal1, signal2"
              className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
            />
            <p className="mt-1 text-xs text-zinc-500">
              Comma-separated. These are public inputs to the ZK circuit.
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-1.5">
              External Nullifier
            </label>
            <input
              type="text"
              value={nullifier}
              onChange={(e) => setNullifier(e.target.value)}
              required
              placeholder="ext-null-001"
              className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
            />
            <p className="mt-1 text-xs text-zinc-500">
              Prevents double-signaling within a scope (e.g., one vote per
              proposal).
            </p>
          </div>

          <button
            type="submit"
            disabled={submitting || !isLoggedIn}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-black transition hover:bg-cyan-400 disabled:opacity-50"
          >
            {submitting ? "Submitting..." : "Submit Proof Request"}
          </button>
        </form>
      </div>
    </div>
  );
}
