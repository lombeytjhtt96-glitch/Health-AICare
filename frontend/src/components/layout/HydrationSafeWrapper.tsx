// src/components/layout/HydrationSafeWrapper.tsx
'use client';

import React, { useEffect, useState } from 'react';

interface HydrationSafeWrapperProps {
  children: React.ReactNode;
}

export default function HydrationSafeWrapper({ children }: HydrationSafeWrapperProps) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    // Suppress React hydration errors caused by browser extensions (Bitdefender bis_skin_checked, Grammarly, etc.)
    if (typeof window !== 'undefined') {
      const origError = console.error;
      console.error = (...args: unknown[]) => {
        const msg = typeof args[0] === 'string' ? args[0] : '';
        const secondMsg = typeof args[1] === 'string' ? args[1] : '';
        if (
          msg.includes('bis_skin_checked') ||
          msg.includes('bis_register') ||
          msg.includes('__processed_') ||
          msg.includes('Hydration') ||
          msg.includes('hydrated') ||
          secondMsg.includes('bis_skin_checked') ||
          secondMsg.includes('bis_register')
        ) {
          return;
        }
        origError.apply(console, args);
      };
    }

    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  return (
    <React.Fragment>
      {children}
    </React.Fragment>
  );
}