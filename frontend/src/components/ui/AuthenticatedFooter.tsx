'use client';

import Link from 'next/link';

export default function AuthenticatedFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full bg-white/5 backdrop-blur-sm border-t border-white/10 text-white mt-auto py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          {/* Copyright */}
          <p className="text-xs text-gray-400">
            © {currentYear} Health-AICare. All rights reserved.
          </p>

          {/* Navigation Links */}
          <div className="flex flex-wrap items-center justify-center gap-6 text-sm font-medium">
            <Link 
              href="/about" 
              className="text-white/70 hover:text-white transition-colors duration-200"
            >
              About
            </Link>
            <span className="hidden sm:inline text-white/20">•</span>
            <Link 
              href="/about/features" 
              className="text-white/70 hover:text-white transition-colors duration-200"
            >
              Features
            </Link>
            <span className="hidden sm:inline text-white/20">•</span>
            <Link 
              href="/resources" 
              className="text-white/70 hover:text-white transition-colors duration-200"
            >
              Resources
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
