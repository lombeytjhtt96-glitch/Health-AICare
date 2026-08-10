"use client";

import { motion } from 'framer-motion';
import { CheckGlyph, CompassGlyph, BridgeGlyph, ShieldWaveGlyph } from '@/components/landing/CustomGlyphs';
import { useI18n } from '@/i18n/I18nProvider';

const features = [
  {
    titleKey: 'landing.benefits.card1.title',
    titleFallback: 'Safety Monitoring',
    descKey: 'landing.benefits.card1.desc',
    descFallback: 'Active monitoring for crisis patterns with instant escalation protocols.',
    icon: ShieldWaveGlyph,
    span: "md:col-span-4 lg:col-span-4"
  },
  {
    titleKey: 'landing.benefits.card2.title',
    titleFallback: 'Interactive Exercises',
    descKey: 'landing.benefits.card2.desc',
    descFallback: 'Not just advice—Health-AI guides you through breathing, journaling, and grounding in real-time.',
    icon: CompassGlyph,
    span: "md:col-span-4 lg:col-span-4"
  },
  {
    titleKey: 'landing.benefits.card3.title',
    titleFallback: 'Human-in-the-Loop',
    descKey: 'landing.benefits.card3.desc',
    descFallback: 'Future active integration with verified psychologists ensures that help reaches you proactively when high-risk patterns are detected.',
    icon: BridgeGlyph,
    span: "md:col-span-4 lg:col-span-4"
  }
];

export default function BenefitsSection() {
  const { t } = useI18n();

  return (
    <section id="features" className="min-h-screen flex flex-col justify-center py-20 bg-transparent relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl lg:text-5xl font-bold text-white mb-6">
            {t('landing.benefits.title', 'More than just a chatbot.')}
          </h2>
          <p className="text-slate-400 text-lg leading-relaxed">
            {t('landing.benefits.subtitle', 'Our vision is simple: Getting real humans to reach out before you even know you need them. Health-AICare bridges the gap between AI triage and professional psychologist intervention.')}
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-12 gap-6">
          
          {/* Main Large Feature */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="md:col-span-8 lg:col-span-8 bg-[#021029]/70 backdrop-blur-md rounded-3xl p-8 border border-white/5 relative overflow-hidden group"
          >
             <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:opacity-20 transition-opacity">
                <CompassGlyph className="w-32 h-32 text-[#FFCA40]" />
             </div>
             <div className="relative z-10">
                <div className="w-12 h-12 rounded-xl bg-[#000B1F] flex items-center justify-center mb-6 border border-white/10">
                  <CompassGlyph className="w-6 h-6 text-[#FFCA40]" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">
                  {t('landing.benefits.main.title', 'Personalized Coping Strategies')}
                </h3>
                <p className="text-slate-400 mb-8 max-w-lg">
                  {t('landing.benefits.main.desc', 'Health-AI doesn\'t just listen; it suggests actionable steps based on how you\'re feeling right now. From guided breathing to reframing negative thoughts.')}
                </p>
                <div className="grid grid-cols-2 gap-4">
                   {['Anxiety Management', 'Academic Stress', 'Sleep Hygiene', 'Social Connection'].map((tag) => (
                      <div key={tag} className="flex items-center gap-2 text-sm text-slate-300 bg-[#000B1F]/50 p-3 rounded-lg border border-white/5">
                        <CheckGlyph className="w-4 h-4 text-[#4ADE80]" />
                        {tag}
                      </div>
                   ))}
                </div>
             </div>
          </motion.div>

          {/* Bottom Row - Three Columns */}
          {features.map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 + (idx * 0.1) }}
              className={`${feature.span} bg-[#021029]/70 backdrop-blur-md rounded-3xl p-6 border border-white/5 hover:border-white/10 transition-colors`}
            >
               <feature.icon className="w-8 h-8 text-[#4ADE80] mb-4" />
               <h4 className="text-lg font-bold text-white mb-2">{t(feature.titleKey, feature.titleFallback)}</h4>
               <p className="text-sm text-slate-400">{t(feature.descKey, feature.descFallback)}</p>
            </motion.div>
          ))}

        </div>
      </div>
    </section>
  );
}
