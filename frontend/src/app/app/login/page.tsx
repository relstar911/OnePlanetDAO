"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Globe, ArrowRight, AlertCircle, UserPlus, LogIn } from "lucide-react";
import { useAuth } from "@/lib/auth-context";

type Mode = "login" | "register";

export default function LoginPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [region, setRegion] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "register") {
        await register(userId, password, region || undefined);
      } else {
        await login(userId, password);
      }
      router.push("/app");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : `${mode} failed`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[80vh] items-center justify-center">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <Globe className="mx-auto h-12 w-12 text-cyan-400" strokeWidth={1} />
          <h1 className="mt-4 text-2xl font-bold">Welcome to OnePlanet</h1>
          <p className="mt-2 text-sm text-zinc-400">
            {mode === "login"
              ? "Sign in to participate in global governance"
              : "Create your account to join the DAO"}
          </p>
        </div>

        {/* Mode Tabs */}
        <div className="mb-4 flex rounded-lg border border-white/10 overflow-hidden">
          <button
            type="button"
            onClick={() => { setMode("login"); setError(""); }}
            className={`flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-medium transition ${
              mode === "login"
                ? "bg-cyan-500/10 text-cyan-400 border-b-2 border-cyan-400"
                : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            <LogIn className="h-4 w-4" /> Sign In
          </button>
          <button
            type="button"
            onClick={() => { setMode("register"); setError(""); }}
            className={`flex-1 flex items-center justify-center gap-2 py-2.5 text-sm font-medium transition ${
              mode === "register"
                ? "bg-cyan-500/10 text-cyan-400 border-b-2 border-cyan-400"
                : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            <UserPlus className="h-4 w-4" /> Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="glass rounded-2xl p-8 space-y-5">
          {error && (
            <div className="flex items-center gap-2 rounded-lg bg-red-500/10 border border-red-500/20 px-4 py-3 text-sm text-red-400">
              <AlertCircle className="h-4 w-4 shrink-0" />
              {error}
            </div>
          )}

          <div>
            <label htmlFor="userId" className="block text-sm font-medium text-zinc-300 mb-1.5">
              User ID
            </label>
            <input
              id="userId"
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              required
              placeholder="Choose a unique user ID"
              className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-zinc-300 mb-1.5">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={4}
              placeholder={mode === "register" ? "Min. 4 characters" : "Enter your password"}
              className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
            />
          </div>

          {mode === "register" && (
            <div>
              <label htmlFor="region" className="block text-sm font-medium text-zinc-300 mb-1.5">
                Region <span className="text-zinc-500">(optional)</span>
              </label>
              <input
                id="region"
                type="text"
                value={region}
                onChange={(e) => setRegion(e.target.value)}
                placeholder="e.g. EU, Africa, LATAM"
                className="w-full rounded-lg border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/25"
              />
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="group flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-4 py-2.5 text-sm font-semibold text-black transition hover:bg-cyan-400 disabled:opacity-50"
          >
            {loading
              ? mode === "register" ? "Creating account..." : "Signing in..."
              : mode === "register" ? "Create Account" : "Sign In"}
            {!loading && (
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            )}
          </button>

          <p className="text-center text-xs text-zinc-500">
            One person, one voice. Your identity is protected by zero-knowledge cryptography.
          </p>
        </form>
      </div>
    </div>
  );
}
