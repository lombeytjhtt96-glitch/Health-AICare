"use client";

import { useEffect, useState, Suspense, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession, signIn, signOut } from "next-auth/react";
import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import {
  FiMail,
  FiLock,
  FiEye,
  FiEyeOff,
  FiAlertCircle,
  FiLogIn,
  FiShield,
} from "@/icons";

// ─── Constants ────────────────────────────────────────────────────────────────
/** Admin 2-FA PIN (6 digits). Change here to update the pin. */
const ADMIN_PIN = "123123";

/** Regex: only letters, numbers, dots, and @  (no _ or -) */
const STRICT_EMAIL_REGEX = /^[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9.]+$/;

/** Relaxed regex that also accepts _ and - (for admin accounts) */
const ADMIN_EMAIL_REGEX = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9.]+$/;

function validateEmail(email: string): string | null {
  if (!email) return "Please enter your email address.";
  // Admin accounts may contain _ or -
  if (!ADMIN_EMAIL_REGEX.test(email))
    return "Invalid email format. Please use only letters, numbers, dots, and @.";
  // Warn if using _ or - but NOT admin
  // (we cannot verify role here, so just allow it — backend rejects non-admin)
  return null;
}

// ─── Admin PIN Modal ──────────────────────────────────────────────────────────
function AdminPinModal({
  onSuccess,
  onCancel,
}: {
  onSuccess: () => void;
  onCancel: () => void;
}) {
  const [pin, setPin] = useState(["", "", "", "", "", ""]);
  const [error, setError] = useState<string | null>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    inputRefs.current[0]?.focus();
  }, []);

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return; // digits only
    const next = [...pin];
    next[index] = value.slice(-1);
    setPin(next);
    setError(null);
    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === "Backspace" && !pin[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleVerify = async () => {
    const entered = pin.join("");
    if (entered.length < 6) {
      setError("Please enter all 6 digits.");
      return;
    }
    setIsVerifying(true);
    // Simulate slight delay for UX
    await new Promise((r) => setTimeout(r, 400));
    if (entered === ADMIN_PIN) {
      onSuccess();
    } else {
      setError("Incorrect PIN. Please try again.");
      setPin(["", "", "", "", "", ""]);
      inputRefs.current[0]?.focus();
    }
    setIsVerifying(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0, y: 20 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.9, opacity: 0, y: 20 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
        className="bg-[#001D58] border border-[#FFCA40]/30 rounded-2xl p-8 max-w-sm w-full shadow-2xl"
      >
        {/* Header */}
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-[#FFCA40]/20 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-[#FFCA40]/30">
            <FiShield className="text-[#FFCA40] text-3xl" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-1">Admin Verification</h2>
          <p className="text-white/60 text-sm">
            Enter the 6-digit administrator PIN to continue
          </p>
        </div>

        {/* PIN Inputs */}
        <div className="flex gap-2 justify-center mb-4">
          {pin.map((digit, i) => (
            <input
              key={i}
              ref={(el) => { inputRefs.current[i] = el; }}
              type="password"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(i, e.target.value)}
              onKeyDown={(e) => handleKeyDown(i, e)}
              className={`w-11 h-14 text-center text-2xl font-bold rounded-xl border-2 bg-white/10 text-white outline-none transition-all duration-200 ${
                digit
                  ? "border-[#FFCA40] bg-[#FFCA40]/10"
                  : "border-white/20 focus:border-[#FFCA40]/60"
              }`}
            />
          ))}
        </div>

        {/* Error */}
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-red-400 text-sm text-center mb-4 flex items-center justify-center gap-1"
          >
            <FiAlertCircle className="w-4 h-4" />
            {error}
          </motion.p>
        )}

        {/* Verify Button */}
        <button
          onClick={handleVerify}
          disabled={isVerifying || pin.join("").length < 6}
          className="w-full py-3 bg-gradient-to-r from-[#FFCA40] to-[#FFD700] text-[#001D58] font-bold rounded-xl mb-3 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-[#FFCA40]/30 transition-all"
        >
          {isVerifying ? (
            <span className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-[#001D58] border-t-transparent rounded-full animate-spin" />
              Verifying...
            </span>
          ) : (
            "Verify PIN"
          )}
        </button>

        {/* Cancel */}
        <button
          onClick={onCancel}
          className="w-full py-2 text-white/50 text-sm hover:text-white/80 transition-colors"
        >
          Cancel & Sign Out
        </button>
      </motion.div>
    </motion.div>
  );
}

// ─── Main SignIn Component ────────────────────────────────────────────────────
export default function SignIn() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tipIndex, setTipIndex] = useState(0);

  // Admin 2-FA state
  const [showAdminPin, setShowAdminPin] = useState(false);

  const mentalHealthTips = [
    { icon: "🌱", title: "Growth Mindset",    message: "Every challenge is an opportunity to learn and grow stronger." },
    { icon: "🧘‍♀️", title: "Mindful Moments",   message: "Take a deep breath. Your mental health journey starts with small, mindful moments." },
    { icon: "💪", title: "Inner Strength",    message: "You are stronger than you think. Trust your ability to overcome difficulties." },
    { icon: "🌟", title: "Self-Compassion",   message: "Be kind to yourself. Treat yourself with the same compassion you'd show a good friend." },
    { icon: "🌈", title: "Hope & Healing",    message: "Healing isn't linear. Every step forward, no matter how small, is progress." },
    { icon: "🤝", title: "Connection Matters", message: "You're not alone in this journey. Seeking help is a sign of strength, not weakness." },
  ];

  // ── Redirect logic (after PIN passed) ──────────────────────────────────────
  const doRedirect = (role: string) => {
    if (role === "admin") router.push("/admin/conversations");
    else router.push("/dashboard");
  };

  // Watch session — show PIN step for admin instead of immediate redirect
  useEffect(() => {
    if (status === "authenticated" && session?.user) {
      if (session.user.role === "admin") {
        setShowAdminPin(true); // hold redirect until PIN verified
      } else {
        router.push("/dashboard");
      }
    }
  }, [status, session, router]);

  // Rotate tips every 5 s
  useEffect(() => {
    const id = setInterval(() => setTipIndex((p) => (p + 1) % mentalHealthTips.length), 5000);
    return () => clearInterval(id);
  }, [mentalHealthTips.length]);

  // ── Submit ─────────────────────────────────────────────────────────────────
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    if (!email || !password) {
      setError("Please fill in all fields.");
      setIsLoading(false);
      return;
    }

    const emailError = validateEmail(email);
    if (emailError) {
      setError(emailError);
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
      setIsLoading(false);
      return;
    }

    try {
      const result = await signIn("credentials", { redirect: false, email, password });
      if (result?.error) {
        setError(
          result.error === "CredentialsSignin"
            ? "Invalid email or password. Please try again."
            : `Sign in failed: ${result.error}`
        );
      } else if (!result?.ok) {
        setError("Sign in failed. Please try again.");
      }
      // On success → useEffect picks up session change → shows PIN if admin
    } catch (err: unknown) {
      setError("An unexpected error occurred. Please try again.");
      console.error("Sign in error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  // ── Admin PIN callbacks ────────────────────────────────────────────────────
  const handlePinSuccess = () => {
    setShowAdminPin(false);
    doRedirect("admin");
  };

  const handlePinCancel = async () => {
    setShowAdminPin(false);
    await signOut({ redirect: false });
    setError("Admin verification cancelled. Please sign in again.");
  };

  // ─────────────────────────────────────────────────────────────────────────
  return (
    <>
      {/* Admin PIN overlay */}
      <AnimatePresence>
        {showAdminPin && (
          <AdminPinModal onSuccess={handlePinSuccess} onCancel={handlePinCancel} />
        )}
      </AnimatePresence>

      <div className="min-h-screen bg-transparent flex relative pt-24">
        {/* Left Panel ────────────────────────────────────────────────────── */}
        <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden z-10">
          <div className="flex flex-col justify-between px-12 py-12 w-full">
            {/* Brand */}
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-[#FFCA40]/90 flex items-center justify-center shadow-[0_0_25px_rgba(255,202,64,0.25)]">
                <Image src="/health_aicare_logo.png" alt="HealthAICare" width={28} height={28} className="w-7 h-7" />
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-white/50">HealthAICare • HealthAI</p>
                <h2 className="text-2xl font-bold text-white">Steady support, built for everyone</h2>
              </div>
            </div>

            {/* Tip card */}
            <div className="mt-10 space-y-6">
              <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl p-8 shadow-[0_25px_80px_rgba(0,0,0,0.35)]">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-2xl bg-white/10 flex items-center justify-center text-2xl">
                    {mentalHealthTips[tipIndex].icon}
                  </div>
                  <div>
                    <p className="text-xs text-white/60 uppercase tracking-widest">Daily Reflection</p>
                    <h3 className="text-xl font-semibold text-white">{mentalHealthTips[tipIndex].title}</h3>
                  </div>
                </div>
                <motion.p
                  key={tipIndex}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                  className="text-white/80 text-base leading-relaxed mt-4"
                >
                  &ldquo;{mentalHealthTips[tipIndex].message}&rdquo;
                </motion.p>
                <div className="flex gap-2 mt-6">
                  {mentalHealthTips.map((_, i) => (
                    <button
                      key={i}
                      onClick={() => setTipIndex(i)}
                      aria-label={`View tip ${i + 1}`}
                      className={`h-1.5 rounded-full transition-all duration-300 ${i === tipIndex ? "w-8 bg-[#FFCA40]" : "w-2 bg-white/20 hover:bg-white/40"}`}
                    />
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: "Active users", value: "2,1k" },
                  { label: "Check-ins",   value: "Daily" },
                  { label: "Availability", value: "24/7" },
                ].map((s) => (
                  <div key={s.label} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-center backdrop-blur">
                    <p className="text-lg font-bold text-white">{s.value}</p>
                    <p className="text-xs text-white/60 uppercase tracking-wider">{s.label}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between text-xs text-white/50">
              <span>Confidential by design</span>
              <span>Evidence-based support</span>
              <span>Guided coping tools</span>
            </div>
          </div>
        </div>

        {/* Right Panel — Login Form ───────────────────────────────────────── */}
        <div className="w-full lg:w-1/2 flex items-center justify-center px-4 py-4 lg:px-6 lg:py-6 relative z-10">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="bg-white/8 backdrop-blur-2xl p-6 lg:p-8 rounded-2xl border border-white/15 shadow-2xl max-w-lg w-full"
          >
            {/* Mobile logo */}
            <div className="text-center mb-4 lg:hidden">
              <div className="mx-auto w-12 h-12 bg-linear-to-br from-[#FFCA40] to-[#FFD700] rounded-xl flex items-center justify-center mb-2 shadow-lg">
                <Image src="/health_aicare_logo.png" alt="HealthAICare" width={24} height={24} className="w-6 h-6" />
              </div>
              <h1 className="text-xl font-bold text-white mb-1">Welcome Back</h1>
              <p className="text-white/70 text-sm">Sign in to continue your wellness journey</p>
            </div>

            {/* Desktop header */}
            <div className="text-center mb-5 hidden lg:block">
              <h1 className="text-2xl font-bold text-white mb-2">Welcome Back</h1>
              <p className="text-white/70 text-base">Sign in to continue your wellness journey</p>
            </div>

            {/* URL-param errors */}
            <Suspense fallback={<div className="h-12" />}>
              <ErrorMessage setError={setError} />
            </Suspense>

            {/* Error banner */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-500/15 border border-red-500/30 text-red-300 p-3 rounded-xl mb-4 flex items-center backdrop-blur-sm"
              >
                <FiAlertCircle className="mr-2 shrink-0 w-4 h-4" />
                <span className="text-sm">{error}</span>
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email */}
              <div className="space-y-1">
                <label htmlFor="email" className="block text-sm font-medium text-white/90">
                  Email Address
                </label>
                <div className="relative group">
                  <FiMail className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40 w-4 h-4 group-focus-within:text-[#FFCA40] transition-colors" />
                  <input
                    id="email"
                    name="email"
                    type="text"
                    autoComplete="email"
                    required
                    value={email}
                    onChange={(e) => { setEmail(e.target.value); setError(null); }}
                    className="w-full pl-10 pr-3 py-3 bg-white/8 border border-white/15 rounded-xl text-white placeholder-white/40 focus:ring-2 focus:ring-[#FFCA40]/50 focus:border-[#FFCA40]/50 outline-none transition-all duration-300 backdrop-blur-sm hover:bg-white/10"
                    placeholder="Enter your email address"
                  />
                </div>
                {/* Hint */}
                <p className="text-white/30 text-xs pl-1">
                  Only letters, numbers, dots and @ are allowed (admin accounts may use _ and -)
                </p>
              </div>

              {/* Password */}
              <div className="space-y-1">
                <label htmlFor="password" className="block text-sm font-medium text-white/90">
                  Password
                </label>
                <div className="relative group">
                  <FiLock className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40 w-4 h-4 group-focus-within:text-[#FFCA40] transition-colors" />
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="current-password"
                    required
                    value={password}
                    onChange={(e) => { setPassword(e.target.value); setError(null); }}
                    className="w-full pl-10 pr-10 py-3 bg-white/8 border border-white/15 rounded-xl text-white placeholder-white/40 focus:ring-2 focus:ring-[#FFCA40]/50 focus:border-[#FFCA40]/50 outline-none transition-all duration-300 backdrop-blur-sm hover:bg-white/10"
                    placeholder="Enter your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white/80 transition-colors p-1"
                  >
                    {showPassword ? <FiEyeOff size={18} /> : <FiEye size={18} />}
                  </button>
                </div>
              </div>

              {/* Forgot password */}
              <div className="text-right">
                <Link href="/forgot-password" className="text-sm text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors font-medium">
                  Forgot your password?
                </Link>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center px-4 py-3 bg-linear-to-r from-[#FFCA40] to-[#FFD700] text-[#001D58] font-semibold rounded-xl hover:from-[#FFD700] hover:to-[#FFCA40] focus:outline-none focus:ring-2 focus:ring-[#FFCA40] transition-all duration-300 disabled:opacity-70 disabled:cursor-not-allowed group shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                {isLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-[#001D58]" />
                ) : (
                  <>
                    <FiLogIn className="mr-2 h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                    Sign In
                  </>
                )}
              </button>
            </form>

            {/* Sign up link */}
            <div className="mt-5 text-center">
              <span className="text-white/60 text-sm">
                Don&apos;t have an account?{" "}
                <Link href="/signup" className="text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors font-medium">
                  Create one here
                </Link>
              </span>
            </div>

            {/* Trust strip */}
            <div className="mt-6 pt-4 border-t border-white/10">
              <div className="flex items-center justify-center space-x-4 text-white/40">
                <div className="flex items-center space-x-1">
                  <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
                  <span className="text-xs">Secure Connection</span>
                </div>
                <div className="flex items-center space-x-1">
                  <FiShield className="w-3 h-3" />
                  <span className="text-xs">Privacy Protected</span>
                </div>
              </div>
            </div>

            <p className="text-xs text-center text-white/40 mt-4">
              By signing in, you agree to our{" "}
              <Link href="/terms" className="text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors">Terms of Service</Link>{" "}
              and{" "}
              <Link href="/privacy" className="text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors">Privacy Policy</Link>.
            </p>
          </motion.div>
        </div>
      </div>
    </>
  );
}

// ─── URL-error handler (Suspense-wrapped) ─────────────────────────────────────
function ErrorMessage({ setError }: { setError: (e: string | null) => void }) {
  const searchParams = useSearchParams();
  useEffect(() => {
    const err = searchParams?.get("error");
    if (err) {
      switch (err) {
        case "CredentialsSignin":
          setError("Invalid email or password. Please try again.");
          break;
        case "Configuration":
          setError("There was a problem signing you in. Please try again later.");
          break;
        default:
          setError("An unexpected error occurred. Please try again.");
      }
    }
  }, [searchParams, setError]);
  return null;
}