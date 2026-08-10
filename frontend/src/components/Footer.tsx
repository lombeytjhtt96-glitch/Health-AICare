export function Footer() {
  return (
    <footer className="border-t border-dark-border bg-dark-bg py-12 px-6 text-sm text-slate-400">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
        <div>
          <h4 className="text-white font-semibold mb-3">HealthAICare</h4>
          <p className="text-xs text-slate-400 leading-relaxed">
            Platform pendukung kesehatan mental berbasis agen cerdas proaktif dengan pembuktian transparan on-chain BSC Testnet & Somnia.
          </p>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Layanan Darurat</h4>
          <ul className="text-xs space-y-2 text-slate-400">
            <li>Hotline Kemenkes: <span className="text-health-gold">119 (ext 8)</span></li>
            <li>Hotline Pendampingan: <span className="text-health-gold">0811-2858-000</span></li>
            <li>Into The Light: <span className="text-health-gold">pendampingan@intothelightid.org</span></li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Teknologi</h4>
          <ul className="text-xs space-y-2 text-slate-400">
            <li>Multi-Agent LangGraph</li>
            <li>Google Gemini 3 LLM</li>
            <li>BSC Testnet & Somnia</li>
            <li>k-Anonymity & Differential Privacy</li>
          </ul>
        </div>
        <div>
          <h4 className="text-white font-semibold mb-3">Komunitas</h4>
          <p className="text-xs text-slate-400">
            Dikembangkan untuk mendampingi masyarakat umum secara aman dan terenkripsi.
          </p>
        </div>
      </div>
      <div className="max-w-7xl mx-auto border-t border-dark-border/50 pt-6 text-center text-xs text-slate-500">
        © 2026 HealthAICare. All rights reserved.
      </div>
    </footer>
  );
}
