import {
  Globe,
  ShieldCheck,
  Vote,
  Eye,
  Users,
  Zap,
  ArrowRight,
  Fingerprint,
  Scale,
} from "lucide-react";

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="currentColor"
      className={className}
    >
      <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
    </svg>
  );
}

const FEATURES = [
  {
    icon: Vote,
    title: "Quadratic Voting",
    desc: "One person, one voice. Mathematically fair — minorities are heard, not drowned out.",
  },
  {
    icon: Fingerprint,
    title: "Zero-Knowledge Identity",
    desc: "Prove you're human without revealing who you are. Privacy by cryptography, not policy.",
  },
  {
    icon: ShieldCheck,
    title: "Guardian Recovery",
    desc: "Lost your key? Trusted guardians restore your identity — no central authority needed.",
  },
  {
    icon: Eye,
    title: "Radical Transparency",
    desc: "Every vote, every transaction, every decision — publicly auditable, always.",
  },
  {
    icon: Scale,
    title: "Constitutional Ethics",
    desc: "Values hardcoded into smart contracts. Ethics first — not an afterthought.",
  },
  {
    icon: Users,
    title: "Global Inclusion",
    desc: "Offline paths, multi-language, accessible. From Frankfurt to refugee camps in Lebanon.",
  },
];

const STATS = [
  { value: "15+", label: "API Endpoints" },
  { value: "90%+", label: "Test Coverage" },
  { value: "6", label: "Core Modules" },
  { value: "Open", label: "Source" },
];

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Nav */}
      <nav className="fixed top-0 z-50 w-full glass">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <Globe className="h-6 w-6 text-cyan-400" />
            <span className="text-lg font-bold tracking-tight">
              OnePlanet
            </span>
          </div>
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/relstar911/OnePlanetDAO"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-sm transition hover:bg-white/5"
            >
              <GithubIcon className="h-4 w-4" />
              GitHub
            </a>
            <a
              href="/app"
              className="flex items-center gap-2 rounded-full bg-cyan-500 px-5 py-2 text-sm font-semibold text-black transition hover:bg-cyan-400"
            >
              Launch App
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative flex flex-col items-center justify-center px-6 pt-40 pb-24 text-center">
        {/* Background glow */}
        <div className="pointer-events-none absolute top-20 left-1/2 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-cyan-500/10 blur-[120px] animate-pulse-glow" />
        <div className="pointer-events-none absolute top-40 left-1/3 h-[300px] w-[400px] -translate-x-1/2 rounded-full bg-violet-500/8 blur-[100px] animate-pulse-glow" />

        <div className="animate-float mb-6">
          <Globe className="h-16 w-16 text-cyan-400" strokeWidth={1} />
        </div>

        <h1 className="max-w-4xl text-5xl font-bold leading-tight tracking-tight sm:text-7xl">
          An Operating System for{" "}
          <span className="gradient-text">Planetary Self-Governance</span>
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-relaxed text-zinc-400 sm:text-xl">
          A supranational federation where every human gets one equal voice for
          just 1&#8364;/month. Powered by zero-knowledge cryptography,
          quadratic voting, and radical transparency. Not another blockchain
          project &mdash; the infrastructure for humanity to govern itself.
        </p>

        <div className="mt-10 flex flex-col gap-4 sm:flex-row">
          <a
            href="/app"
            className="group flex items-center gap-2 rounded-full bg-cyan-500 px-8 py-3.5 font-semibold text-black transition hover:bg-cyan-400"
          >
            <Zap className="h-5 w-5" />
            Launch the App
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </a>
          <a
            href="https://github.com/relstar911/OnePlanetDAO"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 rounded-full border border-white/10 px-8 py-3.5 font-semibold transition hover:bg-white/5"
          >
            <GithubIcon className="h-5 w-5" />
            View Source
          </a>
          <a
            href="#features"
            className="flex items-center gap-2 rounded-full border border-white/10 px-8 py-3.5 font-semibold transition hover:bg-white/5"
          >
            Learn More
          </a>
        </div>

        {/* Stats */}
        <div className="mt-20 grid grid-cols-2 gap-8 sm:grid-cols-4">
          {STATS.map((s) => (
            <div key={s.label} className="text-center">
              <div className="text-3xl font-bold text-cyan-400">{s.value}</div>
              <div className="mt-1 text-sm text-zinc-500">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="mx-auto max-w-6xl px-6 py-24">
        <h2 className="mb-4 text-center text-3xl font-bold sm:text-4xl">
          Built on Principles, Not Promises
        </h2>
        <p className="mx-auto mb-16 max-w-2xl text-center text-zinc-400">
          Every module embeds fairness, privacy, and transparency from the first
          line of code.
        </p>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="glass rounded-2xl p-6 transition hover:border-cyan-500/20"
            >
              <f.icon className="mb-4 h-8 w-8 text-cyan-400" strokeWidth={1.5} />
              <h3 className="mb-2 text-lg font-semibold">{f.title}</h3>
              <p className="text-sm leading-relaxed text-zinc-400">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Vision */}
      <section className="mx-auto max-w-4xl px-6 py-24">
        <div className="glass rounded-3xl p-10 sm:p-16 text-center">
          <h2 className="mb-6 text-3xl font-bold sm:text-4xl">The Vision</h2>
          <p className="text-lg leading-relaxed text-zinc-300">
            Imagine a world where every human being &mdash; whether in a
            high-rise in Frankfurt, a tin-roof home in Nairobi, or a refugee
            camp in Lebanon &mdash; can become an equal member of a global
            federation for just 1&#8364; per month. A federation not controlled
            by governments, corporations, or billionaires, but governed equally
            by all. OnePlanet is the digital constitution of a new, supranational
            democracy: where your voice carries mathematically equal weight to
            every other person on this planet, where manipulation is made
            impossible through zero-knowledge cryptography, where a guardian
            network protects your digital identity, and where every cent flows
            transparently into education, climate action, emergency relief, and
            open technology.
          </p>
          <p className="mt-6 text-lg font-medium text-cyan-400">
            &ldquo;It all starts with a single step: one euro, one vote, one
            idea.&rdquo;
          </p>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-4xl px-6 py-24 text-center">
        <h2 className="mb-4 text-3xl font-bold sm:text-4xl">
          Join the Movement
        </h2>
        <p className="mx-auto mb-10 max-w-xl text-zinc-400">
          Whether you&apos;re a developer, designer, legal expert, community
          organizer, or simply someone who believes in a better world &mdash;
          there&apos;s a place for you here.
        </p>
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <a
            href="https://github.com/relstar911/OnePlanetDAO"
            target="_blank"
            rel="noopener noreferrer"
            className="group flex items-center gap-2 rounded-full bg-white px-8 py-3.5 font-semibold text-black transition hover:bg-zinc-200"
          >
            <GithubIcon className="h-5 w-5" />
            Star on GitHub
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </a>
          <a
            href="https://github.com/relstar911/OnePlanetDAO/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 rounded-full border border-white/10 px-8 py-3.5 font-semibold transition hover:bg-white/5"
          >
            Good First Issues
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-white/5 py-8 text-center text-sm text-zinc-500">
        <div className="mx-auto flex max-w-6xl flex-col items-center gap-2 px-6 sm:flex-row sm:justify-between">
          <div className="flex items-center gap-2">
            <Globe className="h-4 w-4 text-cyan-400" />
            <span>OnePlanet DAO</span>
          </div>
          <p>
            Open source. Built for humanity.
          </p>
        </div>
      </footer>
    </div>
  );
}
