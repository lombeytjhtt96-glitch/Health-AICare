"use client";

import React, { useState, useEffect } from 'react';

interface AffectiveGridProps {
  valence: number | null;
  arousal: number | null;
  onChange: (valence: number, arousal: number) => void;
  disabled?: boolean;
}

const EMOTIONS = [
  { name: 'happy', label: 'Senang / Bahagia', emoji: '😊', V: 0.8, A: 0.6, accentClass: 'accent-yellow-400', colorText: 'text-yellow-400' },
  { name: 'calm', label: 'Tenang / Damai', emoji: '😌', V: 0.7, A: -0.6, accentClass: 'accent-emerald-400', colorText: 'text-emerald-400' },
  { name: 'sad', label: 'Sedih / Kecewa', emoji: '😢', V: -0.7, A: -0.5, accentClass: 'accent-blue-400', colorText: 'text-blue-400' },
  { name: 'angry', label: 'Marah / Kesal', emoji: '😡', V: -0.8, A: 0.7, accentClass: 'accent-red-500', colorText: 'text-red-500' },
  { name: 'anxious', label: 'Cemas / Takut', emoji: '😰', V: -0.6, A: 0.5, accentClass: 'accent-purple-400', colorText: 'text-purple-400' }
];

export default function AffectiveGrid({ valence, arousal, onChange, disabled }: AffectiveGridProps) {
  const [intensities, setIntensities] = useState<Record<string, number>>({
    happy: 0,
    calm: 0,
    sad: 0,
    angry: 0,
    anxious: 0
  });

  // Reconstruct sliders when valence/arousal is loaded from backend
  useEffect(() => {
    if (valence === null || arousal === null) {
      setIntensities({ happy: 0, calm: 0, sad: 0, angry: 0, anxious: 0 });
      return;
    }
    
    // Check if the current intensities already match the loaded valence/arousal to avoid loop
    let currentV = 0;
    let currentA = 0;
    const total = Object.values(intensities).reduce((a, b) => a + b, 0);
    if (total > 0) {
      EMOTIONS.forEach(e => {
        currentV += (intensities[e.name] / total) * e.V;
        currentA += (intensities[e.name] / total) * e.A;
      });
    }
    
    const diffV = Math.abs(currentV - valence);
    const diffA = Math.abs(currentA - arousal);
    
    // Only set from outside if the difference is substantial
    if (diffV > 0.05 || diffA > 0.05 || total === 0) {
      const weights: Record<string, number> = {};
      let wTotal = 0;
      EMOTIONS.forEach(e => {
        const d = Math.sqrt(Math.pow(valence - e.V, 2) + Math.pow(arousal - e.A, 2));
        const w = Math.max(0, 1.5 - d);
        weights[e.name] = w;
        wTotal += w;
      });
      
      const newIntensities: Record<string, number> = {};
      EMOTIONS.forEach(e => {
        newIntensities[e.name] = wTotal > 0 ? Math.round((weights[e.name] / wTotal) * 100) : 0;
      });
      setIntensities(newIntensities);
    }
  }, [valence, arousal]);

  const handleSliderChange = (name: string, value: number) => {
    if (disabled) return;
    
    const newIntensities = {
      ...intensities,
      [name]: value
    };
    setIntensities(newIntensities);

    // Calculate Valence and Arousal using weighted average
    const total = Object.values(newIntensities).reduce((a, b) => a + b, 0);
    if (total === 0) {
      onChange(0, 0); // fallback neutral
    } else {
      let finalV = 0;
      let finalA = 0;
      EMOTIONS.forEach(e => {
        finalV += (newIntensities[e.name] / total) * e.V;
        finalA += (newIntensities[e.name] / total) * e.A;
      });
      onChange(parseFloat(finalV.toFixed(2)), parseFloat(finalA.toFixed(2)));
    }
  };

  const getDominantEmotionText = () => {
    const active = Object.entries(intensities).filter(([_, val]) => val > 0);
    if (active.length === 0) return "Bagaimana perasaan Anda hari ini? Geser slider di atas.";
    
    const sorted = [...active].sort((a, b) => b[1] - a[1]);
    const primary = sorted[0];
    const secondary = sorted[1];
    
    const emotionLabels: Record<string, string> = {
      happy: "Senang/Bahagia",
      calm: "Tenang/Damai",
      sad: "Sedih/Kecewa",
      angry: "Marah/Kesal",
      anxious: "Cemas/Takut"
    };
    
    if (secondary && secondary[1] > 20) {
      return `Perasaan dominan: ${emotionLabels[primary[0]]} (${primary[1]}%) & ${emotionLabels[secondary[0]]} (${secondary[1]}%)`;
    }
    return `Perasaan dominan: ${emotionLabels[primary[0]]} (${primary[1]}%)`;
  };

  return (
    <div className="flex flex-col space-y-4 w-full">
      <div className="space-y-3">
        {EMOTIONS.map(e => (
          <div key={e.name} className="flex items-center space-x-3 bg-white/5 p-3 rounded-lg border border-white/5">
            <span className="text-2xl select-none" role="img" aria-label={e.label}>{e.emoji}</span>
            <div className="flex-1 min-w-0">
              <div className="flex justify-between items-center mb-1 text-xs">
                <span className="font-semibold text-gray-200">{e.label}</span>
                <span className={`font-bold ${e.colorText} font-mono`}>{intensities[e.name] || 0}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={intensities[e.name] || 0}
                disabled={disabled}
                onChange={(evt) => handleSliderChange(e.name, parseInt(evt.target.value))}
                className={`w-full h-2 bg-slate-700/60 rounded-lg appearance-none cursor-pointer ${e.accentClass} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
              />
            </div>
          </div>
        ))}
      </div>
      
      <div className="text-center bg-slate-800/40 p-3 rounded-lg border border-white/5">
        <p className="text-sm font-semibold text-[#FFCA40]">
          {getDominantEmotionText()}
        </p>
        <p className="text-[10px] text-gray-500 mt-1 uppercase tracking-widest font-mono">
          Valence: {valence ?? 0} | Arousal: {arousal ?? 0}
        </p>
      </div>
    </div>
  );
}
