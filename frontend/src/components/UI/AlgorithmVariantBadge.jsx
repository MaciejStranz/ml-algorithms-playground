export default function AlgorithmVariantBadge({ code }) {
  if (!code) return null;

  return (
    <span className="inline-flex items-center rounded-lg border border-cyan-800/60 bg-cyan-950/40 px-2.5 py-1 font-mono text-xs font-semibold text-cyan-300">
      {code}
    </span>
  );
}
