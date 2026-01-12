import { useCallback, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { fetchExperimentById, deleteExperiment } from "../../services/experimentService";
import { useResource } from "../../hooks/useResource";

function Badge({ children, variant = "neutral" }) {
  const cls =
    variant === "success"
      ? "bg-emerald-900/40 text-emerald-200 border-emerald-700/60"
      : variant === "danger"
        ? "bg-red-950/40 text-red-200 border-red-800/60"
        : variant === "warn"
          ? "bg-amber-950/40 text-amber-200 border-amber-800/60"
          : "bg-slate-800 text-slate-200 border-slate-700";

  return (
    <span className={`inline-flex items-center rounded-lg border px-3 py-1 text-xs font-semibold ${cls}`}>
      {children}
    </span>
  );
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

function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleString();
}

function statusVariant(status) {
  if (status === "finished") return "success";
  if (status === "failed") return "danger";
  if (status === "running") return "warn";
  return "neutral";
}

function pickPrimaryMetric(experiment) {
  const task = experiment?.task;
  const metrics = experiment?.metrics || {};
  if (task?.endsWith("_classification")) return metrics?.accuracy ?? null;
  if (task === "regression") return metrics?.r2 ?? null;
  return null;
}

export default function ExperimentDetailView({ experimentId }) {
  const navigate = useNavigate();
  const [actionError, setActionError] = useState("");

  const loader = useCallback(
    ({ signal }) => fetchExperimentById(experimentId, { signal }),
    [experimentId]
  );

  const { data: experiment, loading, errorMsg } = useResource(
    loader,
    [loader],
    { fallbackErrorMessage: "Failed to load experiment details." }
  );

  const primaryMetric = useMemo(
    () => (experiment ? pickPrimaryMetric(experiment) : null),
    [experiment]
  );

  const combinedError = errorMsg || actionError;

  async function handleDelete() {
    if (!experiment?.id) return;

    const ok = window.confirm("Delete this experiment? This action cannot be undone.");
    if (!ok) return;

    setActionError("");
    try {
      await deleteExperiment(experiment.id);
      navigate("/", { replace: true });
    } catch (err) {
      const msg = err?.response?.data?.detail || "Failed to delete experiment.";
      setActionError(msg);
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 px-4 py-10">
        <div className="mx-auto w-full max-w-5xl">
          <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
            Loading experiment...
          </div>
        </div>
      </div>
    );
  }

  if (combinedError) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 px-4 py-10">
        <div className="mx-auto w-full max-w-5xl space-y-4">
          <div className="rounded-xl border border-red-800/60 bg-red-950/40 p-4 text-red-200">
            {combinedError}
          </div>
          <Link className="text-slate-200 underline" to="/">
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  if (!experiment) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 px-4 py-10">
      <div className="mx-auto w-full max-w-5xl space-y-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <Link className="text-slate-300 hover:text-white underline" to="/">
              ← Back to experiments
            </Link>

            <h1 className="mt-3 text-3xl font-extrabold text-white">
              Experiment #{experiment.id}
            </h1>

            <div className="mt-2 flex flex-wrap items-center gap-2">
              <Badge variant={statusVariant(experiment.status)}>
                {experiment.status ?? "—"}
              </Badge>
              <Badge>{experiment.task ?? "—"}</Badge>
              <Badge>{experiment.dataset?.name ?? "—"}</Badge>
              <Badge>{experiment.algorithm?.name ?? "—"}</Badge>
            </div>

            <p className="mt-2 text-sm text-slate-300">
              Created at: {formatDate(experiment.created_at)}
            </p>
          </div>

          <button
            type="button"
            onClick={handleDelete}
            className="rounded-lg border border-red-800/60 bg-red-950/30 px-4 py-2 text-sm font-semibold text-red-200 hover:bg-red-950/50 cursor-pointer"
          >
            Delete
          </button>
        </div>

        {/* Summary */}
        <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 space-y-4">
          <h2 className="text-xl font-bold text-white">Summary</h2>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
            <Stat label="Primary metric" value={primaryMetric} />
            <Stat label="Test size" value={experiment.test_size ?? "—"} />
            <Stat label="Random state" value={experiment.random_state ?? "—"} />
          </div>
        </section>

        {/* Hyperparameters */}
        <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 space-y-4">
          <h2 className="text-xl font-bold text-white">Hyperparameters</h2>

          <pre className="overflow-auto rounded-xl bg-slate-950/40 p-4 text-sm text-slate-200">
            {JSON.stringify(experiment.hyperparameters ?? {}, null, 2)}
          </pre>
        </section>

        {/* Metrics */}
        <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 space-y-4">
          <h2 className="text-xl font-bold text-white">Metrics</h2>

          <pre className="overflow-auto rounded-xl bg-slate-950/40 p-4 text-sm text-slate-200">
            {JSON.stringify(experiment.metrics ?? {}, null, 2)}
          </pre>
        </section>

        {/* Predictions (optional) */}
        {experiment.predictions && (
          <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 space-y-4">
            <h2 className="text-xl font-bold text-white">Predictions</h2>
            <pre className="overflow-auto rounded-xl bg-slate-950/40 p-4 text-sm text-slate-200">
              {JSON.stringify(experiment.predictions, null, 2)}
            </pre>
          </section>
        )}
      </div>
    </div>
  );
}
