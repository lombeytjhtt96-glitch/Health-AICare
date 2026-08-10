import type { Metadata } from "next";
import "./globals.css";
import { Inter } from 'next/font/google'
import ClientProvider from "@/components/auth/ClientProvider";
import QueryProvider from "@/components/providers/QueryProvider";
import { Suspense } from "react";
import GlobalSkeleton from "@/components/ui/GlobalSkeleton";
import { ClientOnlyToaster } from "@/components/ui/ClientOnlyToaster";
import HydrationSafeWrapper from "@/components/layout/HydrationSafeWrapper";
// AppLayout import is removed from here

const inter = Inter({ subsets: ['latin'] })

const getSiteUrl = (): string => {
  const configuredUrl =
    process.env.NEXT_PUBLIC_SITE_URL ??
    process.env.NEXTAUTH_URL ??
    "https://aicare.sumbu.xyz";

  return configuredUrl.startsWith("http") ? configuredUrl : `https://${configuredUrl}`;
};

const siteUrl = getSiteUrl();

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "Health-AICare | AI Mental Health Support",
    template: "%s | Health-AICare",
  },
  description:
    "Health-AICare helps you access earlier mental health support through AI-guided check-ins, supportive conversations, and clear pathways to professional services.",
  keywords: [
    "Health-AICare",
    "mental health support",
    "Health-AI assistant",
    "wellbeing",
    "professional counseling",
    "mental health AI Indonesia",
  ],
  alternates: {
    canonical: siteUrl,
  },
  openGraph: {
    type: "website",
    url: siteUrl,
    siteName: "Health-AICare",
    title: "Health-AICare | AI Mental Health Support",
    description:
      "Self-care and mental health support with proactive AI triage, reflective journaling, and guided access to professional resources.",
    images: [
      {
        url: "/health-aicare_logo.png",
        width: 1200,
        height: 630,
        alt: "Health-AICare platform",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Health-AICare | AI Mental Health Support",
    description:
      "A platform for earlier mental health support, AI-guided conversations, and professional care navigation.",
    images: ["/health-aicare_logo.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-icon.png',
  }
};
// Environment variables type checking
const checkEnvVariables = () => {
  const requiredEnvVars = [
    'NEXTAUTH_SECRET',
    'GOOGLE_CLIENT_ID',
    'GOOGLE_CLIENT_SECRET',
    'NEXTAUTH_URL',
    'INTERNAL_API_KEY',
    'NEXT_PUBLIC_API_URL',
    'ADMIN_EMAIL',
    'ADMIN_PASSWORD'
  ];
  
  console.log("--- Environment Variable Check (Layout) ---");
  requiredEnvVars.forEach(varName => {
    const value = process.env[varName];
    if (!value) {
      console.warn(`[ENV CHECK] Missing required environment variable: ${varName}`);
    } else {
      // For sensitive keys, just log that they are set.
      if (varName.includes('SECRET') || varName.includes('KEY') || varName.includes('PASSWORD')) {
        console.log(`[ENV CHECK] ${varName} is set.`);
      } else {
        console.log(`[ENV CHECK] ${varName}: ${value}`);
      }
    }
  });
  console.log("------------------------------------------");
};

// Run the check only on the server during build/startup
checkEnvVariables();


export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full" suppressHydrationWarning={true}>
      <body
        className={`${inter.className} flex flex-col h-full`}
        suppressHydrationWarning={true}
      >
        <ClientProvider>
          <QueryProvider>
            <HydrationSafeWrapper>
                <Suspense fallback={<GlobalSkeleton />}>
                  {/* AppLayout is removed from here, children are rendered directly */}
                  {children}
                  <ClientOnlyToaster
                    position="top-right"
                    reverseOrder={false}
                    toastOptions={{
                      duration: 5000,
                      style: {
                        background: 'rgba(54, 54, 54, 0.7)',
                        color: '#fff',
                      },
                    }}
                  />
                </Suspense>
            </HydrationSafeWrapper>
          </QueryProvider>
        </ClientProvider>
      </body>
    </html>
  );
}
