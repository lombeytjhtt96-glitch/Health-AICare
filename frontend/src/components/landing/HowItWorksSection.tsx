"use client";

import { motion } from 'framer-motion';
import { useI18n } from '@/i18n/I18nProvider';
import { ArrowScribbleGlyph, CompassGlyph } from '@/components/landing/CustomGlyphs';
import { StarburstGlyph } from '@/components/landing/CustomGlyphs';

export default function HowItWorksSection() {
  const { t } = useI18n();

  return (
    <section className="min-h-screen flex flex-col justify-center py-20 bg-transparent relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#FFCA40] opacity-[0.03] blur-[100px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        <div className="mb-20 text-center">
           <h2 className="text-3xl lg:text-5xl font-bold text-white mb-6 leading-tight">
             {t('landing.how.title', 'Intelligent Intervention Flow')}
           </h2>
           <p className="text-slate-400 text-lg max-w-2xl mx-auto">
             {t('landing.how.subtitle', 'Unlike generic chatbots, HealthAI actively assesses risk and routes you to the right care.')}
           </p>
        </div>

        <div className="max-w-2xl mx-auto">
            <motion.div 
               initial={{ opacity: 0, y: 20 }}
               whileInView={{ opacity: 1, y: 0 }}
               viewport={{ once: true }}
               transition={{ delay: 0.2 }}
               className="p-8 rounded-3xl border border-[#FFCA40]/30 bg-[#021029]/70 backdrop-blur-md shadow-[0_0_40px_-10px_rgba(255,202,64,0.1)]"
            >
               <h3 className="text-sm font-bold text-[#FFCA40] uppercase tracking-widest mb-6 flex items-center gap-2">
                  <StarburstGlyph className="w-4 h-4" />
                  The HealthAI Difference
               </h3>
               
               {/* Interactive Flow Diagram */}
               <div className="relative space-y-6">
                  <div className="absolute left-4 top-4 bottom-4 w-0.5 bg-gradient-to-b from-[#FFCA40]/50 to-transparent" />
                  
                  {[{
                     title: "1. Distress Detection",
                     desc: "Analyzes clinical keywords (e.g., 'hopeless', 'overwhelmed') in real-time.",
                     icon: StarburstGlyph
                  }, {
                      title: "2. Active Intervention",
                      desc: "Immediately deploys CBT-based grounding tools to stabilize emotion.",
                      icon: CompassGlyph
                  }, {
                      title: "3. Professional Handoff",
                      desc: "Summarizes the session and securely forwards it to verified psychologists.",
                      icon: ArrowScribbleGlyph
                  }].map((step, idx) => (
                     <div key={idx} className="relative flex gap-4">
                        <div className="w-8 h-8 rounded-full bg-[#000B1F] border border-[#FFCA40] flex items-center justify-center shrink-0 z-10">
                           <step.icon className="w-4 h-4 text-[#FFCA40]" />
                        </div>
                        <div>
                           <h4 className="text-white font-bold">{step.title}</h4>
                           <p className="text-sm text-slate-400 leading-relaxed">{step.desc}</p>
                        </div>
                     </div>
                  ))}
               </div>
            </motion.div>
        </div>

      </div>
    </section>
  );
}
