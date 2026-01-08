import {
  fetchExperiments,
  deleteExperiment,
} from "../../services/experimentService";
import ExperimentCard from "./ExperimentCard";
import { useEffect, useState } from "react";

export default function ExperimentsList() {
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      setLoading(true);
      setErrorMsg("");

      try {
        const data = await fetchExperiments({ signal: controller.signal });
        console.log("experiments response:", data);
        console.log("isArray:", Array.isArray(data), "length:", data?.length);
        const items = Array.isArray(data) ? data : (data?.results ?? []);
        setExperiments(items);
      } catch (err) {
        if (err?.code === "ERR_CANCELED") return;

        const msg =
          err?.response?.data?.detail ||
          "Failed to load experiments. Please try again.";
        setErrorMsg(msg);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, []);

  const handleDelete = async (experiment) => {
    const ok = window.confirm(
      `Delete experiment #${experiment.id}? This cannot be undone.`
    );
    if (!ok) return;

    setDeletingId(experiment.id);
    setErrorMsg("");

    try {
      await deleteExperiment(experiment.id);
      setExperiments((prev) => prev.filter((e) => e.id !== experiment.id));
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        "Failed to delete experiment. Please try again.";
      setErrorMsg(msg);
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
        Loading experiments...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {errorMsg && (
        <div className="rounded-xl border border-red-800/60 bg-red-950/40 p-4 text-red-200">
          {errorMsg}
        </div>
      )}

      {experiments.length === 0 ? (
        <div className="rounded-xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
          No experiments yet.
        </div>
      ) : (
        experiments.map((exp) => (
          <ExperimentCard
            key={exp.id}
            experiment={exp}
            onDelete={handleDelete}
            deleting={deletingId === exp.id}
          />
        ))
      )}
    </div>
  );
}
