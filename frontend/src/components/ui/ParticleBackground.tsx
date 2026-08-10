
interface ParticleBackgroundProps {
  count?: number;
  colors?: string[];
  minSize?: number;
  maxSize?: number;
  speed?: number;
}

export default function ParticleBackground(props?: ParticleBackgroundProps) {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-[-5]">
      {/* Soft glowing ambient lights (static, GPU accelerated, extremely lightweight) */}
      <div className="absolute top-[-20%] right-[-20%] w-[60vw] h-[60vw] rounded-full bg-blue-500/10 blur-[150px]" />
      <div className="absolute bottom-[-20%] left-[-20%] w-[60vw] h-[60vw] rounded-full bg-[#FFCA40]/5 blur-[150px]" />
    </div>
  );
}