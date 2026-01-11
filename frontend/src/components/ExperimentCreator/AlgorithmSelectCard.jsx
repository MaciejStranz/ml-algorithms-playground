export default function AlgorithmSelectCard({ algorithm, selected, onSelect }) {
  return (
    <button
      type="button"
      onClick={() => onSelect(algorithm.id)}
      className={[
        "w-full text-left rounded-2xl border p-5 shadow-sm transition cursor-pointer",
        "bg-slate-900/60 hover:bg-slate-900/80",
        selected
          ? "border-emerald-500/70 ring-2 ring-emerald-500/40"
          : "border-slate-700",
      ].join(" ")}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-sm text-slate-400">{algorithm.code}</div>
          <h3 className="mt-1 text-lg font-semibold text-white">
            {algorithm.name}
          </h3>

          {algorithm.description && (
            <p className="mt-2 text-sm text-slate-300">
              {algorithm.description}
            </p>
          )}
        </div>

        {algorithm.kind && (
          <span className="rounded-md bg-slate-800 px-2 py-1 text-xs font-semibold text-slate-200">
            {algorithm.kind}
          </span>
        )}
      </div>
    </button>
  );
}
