import { fetchExperiments } from "../../services/experimentService";

function getPrimaryMetric(experiment) {
  const task = (experiment.task || "").toLowerCase();
  const metrics = experiment.metrics || {};

  const isRegression = task.includes("regression");

  if (isRegression) {
    const r2 = metrics.r2;
    return typeof r2 === "number"
      ? { label: "R²", value: r2.toFixed(4) }
      : { label: "R²", value: "—" };
  }

  const acc = metrics.accuracy;
  return typeof acc === "number"
    ? { label: "Accuracy", value: `${(acc * 100).toFixed(1)}%` }
    : { label: "Accuracy", value: "—" };
}

export default function ExperimentCard({ experiment, onDelete, deleting }) {
  const metric = getPrimaryMetric(experiment);

  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-sm text-slate-400">
            Experiment #{experiment.id}
          </div>

          <h3 className="mt-1 text-lg font-semibold text-white">
            {experiment.algorithm?.name ?? "Unknown algorithm"}
          </h3>

          <p className="mt-1 text-slate-300">
            Dataset:{" "}
            <span className="text-slate-200">
              {experiment.dataset?.name ?? "—"}
            </span>
          </p>
        </div>

        <div className="flex flex-col items-end gap-2">
          <span className="rounded-md bg-slate-800 px-2 py-1 text-sm text-slate-200">
            {experiment.status}
          </span>

          <button
            type="button"
            onClick={() => onDelete(experiment)}
            disabled={deleting}
            className="rounded-lg border border-red-800/60 bg-red-950/30 px-3 py-1.5 text-sm font-semibold text-red-200 hover:bg-red-950/50 disabled:opacity-50 disabled:cursor-not-allowed transition"
            title="Delete experiment"
          >
            {deleting ? "Deleting..." : "Delete"}
          </button>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div className="rounded-xl bg-slate-950/40 p-3">
          <div className="text-xs text-slate-400">Task</div>
          <div className="mt-1 text-sm font-medium text-slate-200">
            {experiment.task ?? "—"}
          </div>
        </div>

        <div className="rounded-xl bg-slate-950/40 p-3">
          <div className="text-xs text-slate-400">{metric.label}</div>
          <div className="mt-1 text-sm font-medium text-slate-200">
            {metric.value}
          </div>
        </div>

        <div className="rounded-xl bg-slate-950/40 p-3">
          <div className="text-xs text-slate-400">Created</div>
          <div className="mt-1 text-sm font-medium text-slate-200">
            {experiment.created_at
              ? new Date(experiment.created_at).toLocaleString()
              : "—"}
          </div>
        </div>
      </div>
    </div>
  );
}
