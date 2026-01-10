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
        isDeep ? "bg-indigo-900/40 text-indigo-200" : "bg-slate-800 text-slate-200",
      ].join(" ")}
    >
      {kind ?? "—"}
    </span>
  );
}

function TaskBadge({ task }) {
  return (
    <span className="rounded-md bg-slate-800 px-2 py-1 text-xs font-semibold text-slate-200">
      {formatTask(task)}
    </span>
  );
}

export default function AlgorithmCard({ algorithm }) {
  const specs = Array.isArray(algorithm.hyperparameter_specs)
    ? algorithm.hyperparameter_specs
    : [];

  const supportedTasks = uniq(
    specs.flatMap((s) => (Array.isArray(s.applicable_tasks) ? s.applicable_tasks : []))
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

      <div className="mt-4 flex flex-wrap items-center gap-2">
        {supportedTasks.length > 0 ? (
          supportedTasks.map((t) => <TaskBadge key={t} task={t} />)
        ) : (
          <span className="text-sm text-slate-300">Tasks: —</span>
        )}
      </div>

      <div className="mt-4 text-sm text-slate-300">
        Hyperparameters:{" "}
        <span className="font-semibold text-slate-200">{specs.length}</span>
      </div>
    </div>
  );
}
