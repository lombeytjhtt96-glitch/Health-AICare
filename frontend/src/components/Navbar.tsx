"use client";

import Link from "next/link";
import { Shield, Sparkles, BookOpen, Award, UserCheck, Activity } from "lucide-react";

export function Navbar() {

  return (
    <nav className="glass-card sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-dark-border">
      <Link href="/" className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-ugm-deep to-ugm-blue flex items-center justify-center border border-ugm-gold/30 pulse-glow">
          <Shield className="w-6 h-6 text-ugm-gold" />
        </div>
        <div>
          <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-ugm-gold bg-clip-text text-transparent">
            Health-AICare
          </span>
          <span className="block text-[10px] text-ugm-gold font-medium uppercase tracking-widest">
            Mental Health Companion
          </span>
        </div>
      </Link>

      <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
        <Link href="/health_ai" className="hover:text-ugm-gold transition flex items-center gap-1.5">
          <Sparkles className="w-4 h-4 text-ugm-gold" /> Health-AI Chat
        </Link>
        <Link href="/journaling" className="hover:text-ugm-gold transition flex items-center gap-1.5">
          <BookOpen className="w-4 h-4 text-blue-400" /> Jurnal
        </Link>
        <Link href="/quests" className="hover:text-ugm-gold transition flex items-center gap-1.5">
          <Award className="w-4 h-4 text-amber-400" /> Quests
        </Link>
        <Link href="/admin/dashboard" className="hover:text-ugm-gold transition flex items-center gap-1.5">
          <Activity className="w-4 h-4 text-purple-400" /> Admin
        </Link>
        <Link href="/counselor/dashboard" className="hover:text-ugm-gold transition flex items-center gap-1.5">
          <UserCheck className="w-4 h-4 text-rose-400" /> Counselor
        </Link>
      </div>

      {/* Wallet Connect button removed */}
    </nav>
  );
}
