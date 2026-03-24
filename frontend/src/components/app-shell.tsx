"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Globe,
  Vote,
  LayoutDashboard,
  LogOut,
  User,
  Shield,
  Menu,
  X,
  Home,
} from "lucide-react";
import { useAuth } from "@/lib/auth-context";

const NAV_ITEMS = [
  { href: "/app", label: "Dashboard", icon: LayoutDashboard },
  { href: "/app/vote", label: "Voting", icon: Vote },
  { href: "/app/identity", label: "Identity", icon: Shield },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { isLoggedIn, userId, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const sidebarContent = (
    <>
      {/* Logo */}
      <Link
        href="/"
        className="flex items-center gap-2 px-5 py-5 border-b border-white/5"
        onClick={() => setSidebarOpen(false)}
      >
        <Globe className="h-6 w-6 text-cyan-400" />
        <span className="text-lg font-bold tracking-tight">OnePlanet</span>
      </Link>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setSidebarOpen(false)}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                active
                  ? "bg-cyan-500/10 text-cyan-400"
                  : "text-zinc-400 hover:bg-white/5 hover:text-white"
              }`}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}

        <div className="pt-3 border-t border-white/5 mt-3">
          <Link
            href="/"
            onClick={() => setSidebarOpen(false)}
            className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-zinc-500 hover:bg-white/5 hover:text-white transition"
          >
            <Home className="h-4 w-4" />
            Back to Homepage
          </Link>
        </div>
      </nav>

      {/* User */}
      <div className="border-t border-white/5 p-4">
        {isLoggedIn ? (
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm text-zinc-400">
              <User className="h-4 w-4" />
              <span className="truncate">{userId}</span>
            </div>
            <button
              onClick={() => {
                logout();
                setSidebarOpen(false);
              }}
              className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-zinc-500 transition hover:bg-white/5 hover:text-red-400"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        ) : (
          <Link
            href="/app/login"
            onClick={() => setSidebarOpen(false)}
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-cyan-500 px-3 py-2 text-sm font-semibold text-black transition hover:bg-cyan-400"
          >
            Login
          </Link>
        )}
      </div>
    </>
  );

  return (
    <div className="flex min-h-screen">
      {/* Mobile topbar */}
      <div className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between border-b border-white/5 bg-[#0d0d0d] px-4 py-3 md:hidden">
        <Link href="/" className="flex items-center gap-2">
          <Globe className="h-5 w-5 text-cyan-400" />
          <span className="font-bold">OnePlanet</span>
        </Link>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="rounded-lg p-2 text-zinc-400 hover:bg-white/5"
        >
          {sidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/60 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar – desktop: always visible, mobile: slide-in */}
      <aside
        className={`fixed left-0 top-0 z-40 flex h-full w-60 flex-col bg-[#0d0d0d] border-r border-white/5 transition-transform duration-200 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0`}
      >
        {sidebarContent}
      </aside>

      {/* Main */}
      <main className="flex-1 pt-14 md:pt-0 md:ml-60 p-6 md:p-8">{children}</main>
    </div>
  );
}
