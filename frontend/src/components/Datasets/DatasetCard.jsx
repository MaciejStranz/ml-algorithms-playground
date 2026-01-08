function formatListPreview(list, max = 6) {
  if (!Array.isArray(list) || list.length === 0) return "—";
  const shown = list.slice(0, max);
  const rest = list.length - shown.length;
  return rest > 0 ? `${shown.join(", ")} (+${rest} more)` : shown.join(", ");
}

function Stat({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-950/40 p-4">
      <div className="text-xs text-slate-400">{label}</div>
      <div className="mt-1 text-sm font-medium text-slate-200">
        {value ?? "—"}
      </div>
    </div>
  );
}

export default function DatasetCard({ dataset }) {
  const isClassification =
    typeof dataset?.task === "string" &&
    dataset.task.toLowerCase().includes("classification");

  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-sm text-slate-400">
            {dataset.code ? dataset.code : `Dataset #${dataset.id}`}
          </div>

          <h3 className="mt-1 text-lg font-semibold text-white">
            {dataset.name ?? "Unnamed dataset"}
          </h3>
        </div>

        {dataset.task && (
          <span className="rounded-lg bg-slate-800 px-3 py-1 text-sm font-semibold text-slate-200">
            {dataset.task}
          </span>
        )}
      </div>

      <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Stat label="Samples" value={dataset.n_samples ?? "—"} />
        <Stat label="Features" value={dataset.n_features ?? "—"} />

        {isClassification ? (
          <Stat label="Classes" value={dataset.n_classes ?? "—"} />
        ) : (
          <Stat label="Target" value={dataset.target_name ?? "—"} />
        )}
      </div>

      <div className="mt-4 space-y-3">
        {isClassification && (
          <div className="rounded-xl bg-slate-950/40 p-4">
            <div className="text-xs text-slate-400">Class labels</div>
            <div className="mt-1 text-sm text-slate-200">
              {formatListPreview(dataset.class_labels)}
            </div>
          </div>
        )}

        <div className="rounded-xl bg-slate-950/40 p-4">
          <div className="text-xs text-slate-400">Feature names</div>
          <div className="mt-1 text-sm text-slate-200">
            {formatListPreview(dataset.feature_names)}
          </div>
        </div>
      </div>
    </div>
  );
}
