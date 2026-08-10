"use client";

import { usePathname } from "next/navigation";
import { useSession } from "next-auth/react";
import Footer from "./Footer";
import MinimalFooter from "./MinimalFooter";
import AuthenticatedFooter from "./AuthenticatedFooter";

/**
 * Smart footer wrapper that displays the appropriate footer based on context:
 * - Full footer: Landing page only (marketing context)
 * - Minimal footer: Auth pages, static content pages (about, privacy, terms, resources)
 * - Authenticated footer: Logged-in app pages
 * - No footer: Immersive pages (HealthAI chat, CareQuest, admin/counselor dashboards)
 */
export default function FooterWrapper() {
  const pathname = usePathname();
  const { status } = useSession();
  const isAuthenticated = status === "authenticated";

  // Pages that should NEVER have a footer (immersive experiences)
  const noFooterPages = [
    '/health_ai',
    '/carequest',
    '/admin',
    '/counselor',
  ];

  // Check if current path starts with any no-footer prefix
  const isNoFooterPage = noFooterPages.some(page => pathname?.startsWith(page));

  // If user is authenticated/logged in
  if (isAuthenticated) {
    if (isNoFooterPage) {
      return null;
    }
    return <AuthenticatedFooter />;
  }

  // If user is not authenticated (anonymous public visitor)
  if (isNoFooterPage) {
    return null;
  }

  // Pages that get the FULL footer (marketing/landing context)
  const fullFooterPages = ['/'];
  const isFullFooterPage = fullFooterPages.includes(pathname || '');

  // Landing page gets full footer
  if (isFullFooterPage) {
    return <Footer />;
  }

  // Auth pages and static content pages get minimal footer
  const minimalFooterPages = [
    '/signin',
    '/signup',
    '/forgot-password',
    '/reset-password',
    '/about',
    '/privacy',
    '/terms',
    '/access-denied',
  ];
  const isMinimalFooterPage = minimalFooterPages.some(page => pathname?.startsWith(page));
  
  if (isMinimalFooterPage) {
    return <MinimalFooter />;
  }

  // Default for unauthenticated: minimal footer
  return <MinimalFooter />;
}