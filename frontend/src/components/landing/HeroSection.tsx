"use client";

import Link from 'next/link';
import { motion, useReducedMotion } from 'framer-motion';
import type { Variants } from 'framer-motion';
import { ArrowScribbleGlyph, StarburstGlyph } from '@/components/landing/CustomGlyphs';
import ParticleBackground from '@/components/ui/ParticleBackground';
import { useI18n } from '@/i18n/I18nProvider';

// Animation variants for staggered entrance
const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

const itemVariants: Variants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: { type: "spring", stiffness: 50, damping: 20 }
  }
};

export default function HeroSection() {
  const shouldReduceMotion = useReducedMotion();
  const { t } = useI18n();

  return (
    <section className="relative min-h-screen flex items-center overflow-hidden bg-transparent">
      
      {/* 1. Background Layers */}
      {/* Subtle Image Backdrop removed as requested */}

      {/* Particle System - kept subtle */}
      <div className="absolute inset-0 z-0 pointer-events-none h-[120vh]">
        <ParticleBackground
          count={shouldReduceMotion ? 0 : 50}
          colors={["#FFCA40", "#6A98F0", "#ffffff"]}
          minSize={2}
          maxSize={8}
          speed={1}
        />
      </div>

      {/* Grid Pattern Overlay for "Tech/Structural" feel */}
      <div className="absolute inset-0 z-0 opacity-[0.03] bg-[linear-gradient(to_right,#ffffff_1px,transparent_1px),linear-gradient(to_bottom,#ffffff_1px,transparent_1px)] bg-size-[4rem_4rem] h-[200vh]" />

      {/* 2. Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 z-20 w-full pt-20 pb-16 lg:pt-32 lg:pb-24">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center text-center max-w-3xl mx-auto"
        >
          {/* Left Column: Typography & CTA */}
          <div className="space-y-8">
            
            {/* Headline */}
            <div className="space-y-4">
              <motion.h1 
                variants={itemVariants}
                className="text-4xl sm:text-5xl lg:text-7xl font-bold text-white leading-[1.1] tracking-tight"
              >
                {t('landing.hero.title_line1', 'Your mental health,')}
                <br />
                <span className="text-[#FFCA40]">
                  {t('landing.hero.title_highlight', 'proactively managed.')}
                </span>
              </motion.h1>
              
              <motion.p 
                variants={itemVariants}
                className="text-lg sm:text-xl text-slate-300 leading-relaxed max-w-lg mx-auto font-light"
              >
                {t(
                  'landing.hero.description',
                  "Health-AI is an intelligent agent designed to support your mental health. It helps you unpack your thoughts, find coping mechanisms, and connect with professional help when you're ready."
                )}
              </motion.p>
            </div>

            {/* CTAs */}
            <motion.div 
              variants={itemVariants}
              className="flex flex-col sm:flex-row gap-4 justify-center pt-4"
            >
              <Link href="/health_ai" className="w-full sm:w-auto">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full sm:w-auto px-8 py-4 bg-[#FFCA40] text-[#000B1F] rounded-xl font-bold text-lg shadow-[0_0_20px_rgba(255,202,64,0.3)] hover:shadow-[0_0_30px_rgba(255,202,64,0.5)] transition-all flex items-center justify-center gap-2"
                >
                  {t('landing.hero.cta_primary', 'Chat with Health-AI')}
                  <ArrowScribbleGlyph className="w-5 h-5" />
                </motion.button>
              </Link>
              
              <Link href="/about" className="w-full sm:w-auto">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full sm:w-auto px-8 py-4 bg-transparent border border-white/20 text-white rounded-xl font-semibold text-lg hover:bg-white/5 transition-all"
                >
                  {t('landing.hero.cta_secondary', 'How it works')}
                </motion.button>
              </Link>
            </motion.div>

          </div>
        </motion.div>
      </div>
    </section>
  );
}