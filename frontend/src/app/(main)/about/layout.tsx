import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "About",
  description:
    "Learn how Health-AICare supports earlier mental health intervention for students through AI triage, reflective tools, and counselor-connected workflows.",
  alternates: {
    canonical: "/about",
  },
  openGraph: {
    title: "About Health-AICare",
    description:
      "Explore the student-first design, safety architecture, and research foundations behind Health-AICare.",
    url: "/about",
    type: "website",
  },
  twitter: {
    title: "About Health-AICare",
    description:
      "How Health-AICare combines proactive AI support with campus mental health pathways.",
  },
};

export default function AboutLayout({ children }: { children: ReactNode }) {
  return children;
}
