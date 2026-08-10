"use client";

import { useState, useEffect } from "react";
import { useSession, signOut } from "next-auth/react";
import Image from "next/image";
import Link from "next/link";
import { HiMenu, HiViewGrid } from "react-icons/hi"; // Added HiViewGrid for Dashboard icon

import { useWellnessState } from "@/hooks/useQuests";
import { useProfilePicture } from "@/hooks/useProfilePicture";
import MobileNavMenu from "./MobileNavMenu";
import ProfileDropdown from "./ProfileDropdown";

interface HeaderProps {
  onToggleSidebar: () => void;
}

export default function Header({ onToggleSidebar }: HeaderProps) {
  const { data: session, status } = useSession();
  const { data: wellness } = useWellnessState();
  const { src: profilePictureSrc } = useProfilePicture();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Track scroll position
  useEffect(() => {
    const scrollContainer = document.getElementById("app-scroll-container");
    const target: (Window & typeof globalThis) | HTMLElement = scrollContainer ?? window;

    const getScrollTop = () => {
      if (target === window) {
        return window.scrollY;
      }
      return (target as HTMLElement).scrollTop;
    };

    const handleScroll = () => {
      setScrolled(getScrollTop() > 10);
    };

    handleScroll();
    target.addEventListener("scroll", handleScroll, { passive: true } as AddEventListenerOptions);

    return () => {
      target.removeEventListener("scroll", handleScroll as EventListener);
    };
  }, []);

  const toggleProfile = () => {
    setIsProfileOpen(!isProfileOpen);
    if (isMobileMenuOpen) setIsMobileMenuOpen(false);
  };

  const handleSignOut = () => {
    signOut({ callbackUrl: "/" });
  };

  const navLinks = [
    { href: "/health_ai", label: "Talk to HealthAI" }, // Added Talk to HealthAI
    { href: "/about", label: "About" },
    { href: "/about/features", label: "Features" },
  ];

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-100 transition-all duration-500 ease-in-out ${scrolled
          ? "bg-[#001D58]/70 backdrop-blur-md border-b border-white/10 py-3 shadow-lg supports-backdrop-filter:bg-[#001D58]/60"
          : "bg-transparent py-5"
          }`}
      >
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">

            {/* Left Section: Logo & Nav */}
            <div className="flex items-center gap-8">
              {/* Primary Menu Trigger (left-aligned for visibility) */}
              {status === "authenticated" && (
                <>
                  <button
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    className="md:hidden inline-flex items-center gap-2 px-3 py-2 rounded-full border border-[#FFCA40]/30 bg-[#FFCA40]/10 text-[#FFCA40] hover:bg-[#FFCA40]/20 transition-all duration-200"
                    aria-label="Open menu"
                  >
                    <HiMenu className="w-5 h-5" />
                    <span className="text-xs font-semibold uppercase tracking-wider">Menu</span>
                  </button>

                  <button
                    onClick={onToggleSidebar}
                    className="hidden md:inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-[#FFCA40]/30 bg-[#FFCA40]/10 text-[#FFCA40] hover:bg-[#FFCA40]/20 hover:border-[#FFCA40]/50 transition-all duration-200"
                    aria-label="Open sidebar menu"
                  >
                    <HiMenu className="w-4 h-4" />
                    <span className="text-xs font-semibold uppercase tracking-wider">Menu</span>
                  </button>
                </>
              )}

              {/* Logo */}
              <Link href="/" className="flex items-center gap-3 group">
                <div className="relative w-9 h-9 overflow-hidden rounded-full border-2 border-white/20 group-hover:border-[#FFCA40] transition-colors duration-300 shadow-md">
                  <img
                    src="/health_aicare_logo.png?v=2"
                    alt="HealthAICare Logo"
                    className="object-cover w-full h-full"
                  />
                </div>
                <div className="flex flex-col">
                  <span className="text-base font-bold leading-none text-white tracking-wide group-hover:text-[#FFCA40] transition-colors">
                    HealthAICare
                  </span>
                  <span className="text-[9px] uppercase tracking-widest text-white/60 font-medium mt-0.5">
                    Mental Health
                  </span>
                </div>
              </Link>

              {/* Desktop Nav Links */}
              {status !== "authenticated" && (
                <nav className="hidden md:flex items-center gap-6">
                  {navLinks.map((item) => (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`text-sm font-medium transition-colors duration-200 relative group ${item.href === '/health_ai' ? 'text-[#FFCA40] hover:text-[#FFCA40]/80' : 'text-white/70 hover:text-white'
                        }`}
                    >
                      {item.label}
                      <span className={`absolute -bottom-1 left-0 w-0 h-0.5 transition-all duration-300 group-hover:w-full opacity-0 group-hover:opacity-100 ${item.href === '/health_ai' ? 'bg-[#FFCA40]' : 'bg-white'
                        }`} />
                    </Link>
                  ))}
                </nav>
              )}
            </div>

            {/* Right Section: Actions */}
            <div className="flex items-center gap-4">
              {status === "authenticated" ? (
                <>
                  {/* Dashboard Button (Desktop) */}
                  <Link
                    href="/dashboard"
                    className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20 transition-all duration-200 text-white/80 group"
                  >
                    <HiViewGrid className="w-4 h-4 group-hover:text-[#FFCA40] transition-colors" />
                    <span className="text-xs font-medium uppercase tracking-wider">Dashboard</span>
                  </Link>



                  {/* Profile Dropdown Trigger */}
                  <div className="relative">
                    <button
                      onClick={toggleProfile}
                      aria-haspopup="menu"
                      aria-expanded={isProfileOpen}
                      aria-controls="profile-menu"
                      aria-label="Open profile menu"
                      className={`relative w-9 h-9 rounded-full overflow-hidden border-2 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-[#FFCA40]/50 ${isProfileOpen ? "border-[#FFCA40]" : "border-white/20 hover:border-white/40"
                        }`}
                    >
                      <Image
                        src={profilePictureSrc}
                        alt="Profile"
                        fill
                        className="object-cover"
                      />
                    </button>

                    <ProfileDropdown
                      user={session.user}
                      isOpen={isProfileOpen}
                      wellness={wellness}
                      profilePictureSrc={profilePictureSrc}
                      onClose={() => setIsProfileOpen(false)}
                      onSignOut={handleSignOut}
                    />
                  </div>
                </>
              ) : (
                <div className="flex items-center gap-4">
                  <Link
                    href="/signin"
                    className="text-sm font-medium text-white/80 hover:text-white transition-colors"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="px-5 py-2 bg-white text-[#001D58] rounded-full text-sm font-bold hover:bg-[#FFCA40] transition-colors duration-300 shadow-lg shadow-black/10"
                  >
                    Get Started
                  </Link>
                </div>
              )}

              {/* Mobile menu trigger intentionally moved to left section for visibility */}
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Menu */}
      <MobileNavMenu
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
      />
    </>
  );
}
