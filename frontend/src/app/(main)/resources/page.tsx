"use client";

import Link from "next/link";
import { ShieldAlert, Phone, Calendar, Heart, BookOpen, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export default function ResourcesPage() {
  return (
    <div className="min-h-screen bg-linear-to-b from-[#001D58] to-[#000c24] text-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-10">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/30 text-xs font-semibold text-red-400 mb-4">
              <ShieldAlert className="w-3.5 h-3.5" /> Emergency & Support Guide
            </span>
            <h1 className="text-3.5xl font-extrabold tracking-tight sm:text-4xl bg-gradient-to-r from-white via-white to-gray-400 bg-clip-text text-transparent">
              Support & Crisis Resources
            </h1>
            <p className="mt-3 text-lg text-gray-300 max-w-2xl mx-auto">
              If you are going through a difficult time, please remember that you are not alone. There are people and resources available to help you.
            </p>
          </motion.div>
        </div>

        {/* Warning Banner */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="mb-8 p-6 rounded-3xl bg-red-500/10 border border-red-500/20 flex flex-col md:flex-row items-start gap-4 shadow-2xl"
        >
          <div className="p-3 bg-red-500/20 rounded-2xl text-red-400 shrink-0">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">Butuh bantuan segera?</h2>
            <p className="mt-1 text-sm text-gray-300 leading-relaxed">
              HealthAI adalah pendamping kesehatan mental berbasis kecerdasan buatan dan bukan pengganti layanan darurat medis atau psikologis profesional. Jika Anda berada dalam situasi krisis atau membahayakan diri sendiri, segera hubungi nomor darurat di bawah ini.
            </p>
          </div>
        </motion.div>

        {/* Crisis Hotlines Grid */}
        <h3 className="text-lg font-bold text-[#FFCA40] mb-4">Layanan Darurat & Konseling Krisis</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="p-6 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl hover:bg-white/10 transition-all duration-300"
          >
            <div className="flex justify-between items-start mb-4">
              <span className="p-2.5 bg-[#FFCA40]/10 border border-[#FFCA40]/30 rounded-xl text-[#FFCA40]">
                <Phone className="w-5 h-5" />
              </span>
              <span className="text-xs uppercase bg-[#FFCA40]/10 text-[#FFCA40] px-2 py-0.5 rounded font-semibold">24/7</span>
            </div>
            <h4 className="text-base font-bold text-white">Layanan Darurat Nasional</h4>
            <p className="text-2xl font-black text-[#FFCA40] mt-1">112</p>
            <p className="mt-2 text-xs text-gray-400">
              Layanan darurat bebas pulsa untuk meminta ambulans, kepolisian, atau bantuan darurat lainnya di seluruh Indonesia.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="p-6 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl hover:bg-white/10 transition-all duration-300"
          >
            <div className="flex justify-between items-start mb-4">
              <span className="p-2.5 bg-[#FFCA40]/10 border border-[#FFCA40]/30 rounded-xl text-[#FFCA40]">
                <Phone className="w-5 h-5" />
              </span>
              <span className="text-xs uppercase bg-[#FFCA40]/10 text-[#FFCA40] px-2 py-0.5 rounded font-semibold">24/7</span>
            </div>
            <h4 className="text-base font-bold text-white">Layanan SEJIWA Kemenkes</h4>
            <p className="text-2xl font-black text-[#FFCA40] mt-1">119 (Ext. 8)</p>
            <p className="mt-2 text-xs text-gray-400">
              Layanan konseling kesehatan mental gratis yang disediakan oleh Kementerian Kesehatan RI untuk masyarakat umum.
            </p>
          </motion.div>
        </div>

        {/* Platform Support Services */}
        <h3 className="text-lg font-bold text-white mb-4">Layanan Dukungan HealthAICare</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="p-6 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl hover:border-white/20 transition-all duration-300 flex flex-col justify-between"
          >
            <div>
              <Calendar className="w-6 h-6 text-[#FFCA40] mb-3" />
              <h4 className="text-sm font-bold text-white">Konseling Profesional</h4>
              <p className="mt-1 text-xs text-gray-400 leading-relaxed">
                Jadwalkan sesi konsultasi tatap muka atau daring bersama konselor profesional kami.
              </p>
            </div>
            <Link 
              href="/appointments/book" 
              className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors"
            >
              Book Session <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="p-6 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl hover:border-white/20 transition-all duration-300 flex flex-col justify-between"
          >
            <div>
              <Heart className="w-6 h-6 text-[#FFCA40] mb-3" />
              <h4 className="text-sm font-bold text-white">Latihan Terapi Mandiri</h4>
              <p className="mt-1 text-xs text-gray-400 leading-relaxed">
                Coba latihan pernapasan, relaksasi otot, atau grounding untuk membantu menenangkan pikiran.
              </p>
            </div>
            <Link 
              href="/activities" 
              className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors"
            >
              Try Activities <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="p-6 rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl hover:border-white/20 transition-all duration-300 flex flex-col justify-between"
          >
            <div>
              <BookOpen className="w-6 h-6 text-[#FFCA40] mb-3" />
              <h4 className="text-sm font-bold text-white">Jurnal Refleksi Harian</h4>
              <p className="mt-1 text-xs text-gray-400 leading-relaxed">
                Tuangkan pikiran Anda dalam jurnal aman dan pribadi untuk memproses emosi harian.
              </p>
            </div>
            <Link 
              href="/journaling" 
              className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-[#FFCA40] hover:text-[#FFCA40]/80 transition-colors"
            >
              Open Journal <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </motion.div>

        </div>

      </div>
    </div>
  );
}
