"use client";

import { motion } from "framer-motion";
import { FiMail, FiLock, FiEye, FiEyeOff } from "@/icons";
import { useState } from "react";

interface SignupStep1Props {
  formData: {
    email: string;
    password: string;
    confirmPassword: string;
  };
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onNext: () => void;
}

export default function SignupStep1({ formData, onChange, onNext }: SignupStep1Props) {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const password = formData.password || "";
  const checks = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /\d/.test(password),
    special: /[@$!%*?&]/.test(password),
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onNext();
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Create Your Account</h2>
        <p className="text-white/70 text-sm">
          Let&apos;s start with your email and password
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Email */}
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-white/90 mb-2">
            <FiMail className="inline mr-1" />
            Email Address *
          </label>
          <input
            type="text"
            id="email"
            name="email"
            value={formData.email}
            onChange={onChange}
            required
            pattern="[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9.]+"
            className="w-full px-4 py-3 bg-white/8 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-[#FFCA40] focus:border-[#FFCA40] transition-all duration-200"
            placeholder="yourname@example.com"
          />
          <p className="text-white/40 text-xs mt-1 pl-1">
            Only letters, numbers, dots (.) and @ are allowed. No underscores or hyphens.
          </p>
        </div>

        {/* Password */}
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-white/90 mb-2">
            <FiLock className="inline mr-1" />
            Password *
          </label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              id="password"
              name="password"
              value={formData.password}
              onChange={onChange}
              required
              className="w-full px-4 py-3 pr-12 bg-white/8 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-[#FFCA40] focus:border-[#FFCA40] transition-all duration-200"
              placeholder="Create a strong password"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/40 hover:text-white/80 transition-colors"
            >
              {showPassword ? <FiEyeOff size={18} /> : <FiEye size={18} />}
            </button>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-3 bg-white/5 p-3 rounded-xl border border-white/10">
            {[
              { key: 'length', label: '8+ characters' },
              { key: 'uppercase', label: 'Uppercase letter' },
              { key: 'lowercase', label: 'Lowercase letter' },
              { key: 'number', label: 'Number' },
              { key: 'special', label: 'Special character' },
            ].map((item) => {
              const isMet = checks[item.key as keyof typeof checks];
              return (
                <div
                  key={item.key}
                  className={`flex items-center gap-2 text-xs transition-colors duration-200 ${
                    item.key === 'special' ? 'col-span-2 sm:col-span-1' : ''
                  }`}
                >
                  <span
                    className={`flex items-center justify-center w-4 h-4 rounded-full border transition-all duration-200 text-[10px] font-bold ${
                      isMet
                        ? 'bg-green-500/20 border-green-400 text-green-400 scale-105'
                        : 'border-white/20 text-white/30'
                    }`}
                  >
                    {isMet ? '✓' : '•'}
                  </span>
                  <span className={`transition-colors duration-200 ${isMet ? 'text-green-400 font-medium' : 'text-white/60'}`}>
                    {item.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Confirm Password */}
        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-white/90 mb-2">
            <FiLock className="inline mr-1" />
            Confirm Password *
          </label>
          <div className="relative">
            <input
              type={showConfirmPassword ? "text" : "password"}
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={onChange}
              required
              className="w-full px-4 py-3 pr-12 bg-white/8 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-[#FFCA40] focus:border-[#FFCA40] transition-all duration-200"
              placeholder="Confirm your password"
            />
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/40 hover:text-white/80 transition-colors"
            >
              {showConfirmPassword ? <FiEyeOff size={18} /> : <FiEye size={18} />}
            </button>
          </div>
        </div>

        {/* Next Button */}
        <motion.button
          type="submit"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full bg-linear-to-r from-[#FFCA40] to-[#FFD700] text-[#001D58] font-semibold py-4 px-6 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl hover:from-[#FFD700] hover:to-[#FFCA40]"
        >
          Continue →
        </motion.button>
      </form>
    </motion.div>
  );
}
