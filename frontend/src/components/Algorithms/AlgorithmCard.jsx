function uniq(arr) {
  return Array.from(new Set(arr));
}

function formatTask(task) {
  if (!task) return "—";
  return task.replaceAll("_", " ");
}

function KindBadge({ kind }) {
  const isDeep = kind === "deep";
  return (
    <span
      className={[
        "rounded-md px-2 py-1 text-xs font-semibold",
        isDeep
          ? "bg-indigo-900/40 text-indigo-200"
          : "bg-slate-800 text-slate-200",
      ].join(" ")}
    >
      {kind ?? "—"}
    </span>
  );
}

function TaskBadge({ task }) {
  return (
    <span className="rounded-md bg-indigo-900/30 px-2 py-1 text-xs font-semibold text-indigo-100">
      {formatTask(task)}
    </span>
  );
}

function VariantBadge({ code }) {
  return (
    <span className="rounded-md bg-emerald-900/30 px-2 py-1 text-xs font-semibold text-emerald-100">
      {code}
    </span>
  );
}


export default function AlgorithmCard({ algorithm }) {
  const variants = Array.isArray(algorithm?.variants) ? algorithm.variants : [];

  const supportedTasks = uniq(
    variants.flatMap((v) =>
      Array.isArray(v.supported_tasks) ? v.supported_tasks : [],
    ),
  );

  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold text-white">{algorithm.name}</h3>
          {algorithm.description && (
            <p className="mt-2 text-sm text-slate-300 line-clamp-3">
              {algorithm.description}
            </p>
          )}
        </div>

        <KindBadge kind={algorithm.kind} />
      </div>

      <div className="mt-4 space-y-2">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm font-semibold text-slate-300">
            Supported tasks:
          </span>
          {supportedTasks.length > 0 ? (
            supportedTasks.map((t) => <TaskBadge key={t} task={t} />)
          ) : (
            <span className="text-sm text-slate-400">-</span>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm font-semibold text-slate-300">
            Available variants:
          </span>
          {variants.length > 0 ? (
            variants.map((v) => <VariantBadge key={v.code} code={v.code} />)
          ) : (
            <span className="text-sm text-slate-400">-</span>
          )}
        </div>
      </div>
    </div>
  );
}
