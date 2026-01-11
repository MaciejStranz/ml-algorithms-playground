import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { fetchDatasets } from "../../services/datasetService";
import { fetchAlgorithms } from "../../services/algorithmService";
import { createExperiment } from "../../services/experimentService";
import { useResourceList } from "../../hooks/useResourceList";

import DatasetPicker from "./DatasetPicker";
import AlgorithmPicker from "./AlgorithmPicker";
import HyperparametersForm from "./HyperParametersForm";
import { buildHyperparametersPayload } from "../../utils/hyperparameters";

export default function ExperimentCreatorWizard() {
  const navigate = useNavigate();

  const [datasetId, setDatasetId] = useState("");
  const [algorithmId, setAlgorithmId] = useState("");
  const [hyperparameters, setHyperparameters] = useState({});

  // config
  const [testSize, setTestSize] = useState(0.3);
  const [randomState, setRandomState] = useState(42);
  const [includePredictions, setIncludePredictions] = useState(true);
  const [includeProbabilities, setIncludeProbabilities] = useState(false);

  // submit state
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");

  const {
    items: datasets,
    loading: datasetsLoading,
    errorMsg: datasetsError,
  } = useResourceList(({ signal }) => fetchDatasets({ signal }), []);

  const {
    items: algorithms,
    loading: algorithmsLoading,
    errorMsg: algorithmsError,
  } = useResourceList(({ signal }) => fetchAlgorithms({ signal }), []);

  const selectedDataset = useMemo(
    () => datasets.find((d) => String(d.id) === String(datasetId)),
    [datasets, datasetId]
  );

  const task = selectedDataset?.task;

  const filteredAlgorithms = useMemo(() => {
    if (!task) return [];
    return algorithms.filter((algo) => {
      const specs = Array.isArray(algo.hyperparameter_specs) ? algo.hyperparameter_specs : [];
      return specs.some((s) => Array.isArray(s.applicable_tasks) && s.applicable_tasks.includes(task));
    });
  }, [algorithms, task]);

  const selectedAlgorithm = useMemo(
    () => algorithms.find((a) => String(a.id) === String(algorithmId)),
    [algorithms, algorithmId]
  );

  // reset downstream selection when dataset changes
  useEffect(() => {
    setAlgorithmId("");
    setHyperparameters({});
    setSubmitError("");

    // classification-only option should be reset when task changes
    setIncludeProbabilities(false);
  }, [datasetId]);

  // init hyperparameters defaults when algorithm changes
  useEffect(() => {
    if (!selectedAlgorithm || !task) return;

    const specs = Array.isArray(selectedAlgorithm.hyperparameter_specs)
      ? selectedAlgorithm.hyperparameter_specs
      : [];

    const applicable = specs.filter((s) => {
      const tasks = Array.isArray(s.applicable_tasks) ? s.applicable_tasks : [];
      return tasks.length === 0 || tasks.includes(task);
    });

    const defaults = {};
    for (const s of applicable) {
      if (!s?.name) continue;
      defaults[s.name] = s.default ?? null;
    }

    setHyperparameters(defaults);
    setSubmitError("");
  }, [selectedAlgorithm, task]);

  const errorMsg = datasetsError || algorithmsError;

  const isClassification = task?.endsWith("_classification");
  const canSubmit =
    Boolean(datasetId) &&
    Boolean(algorithmId) &&
    !datasetsLoading &&
    !algorithmsLoading &&
    !submitting;

  async function handleRunExperiment() {
    setSubmitError("");

    if (!datasetId || !algorithmId) {
      setSubmitError("Please select dataset and algorithm first.");
      return;
    }

    // basic client-side validation (keep it light; backend is source of truth)
    if (typeof testSize !== "number" || testSize <= 0 || testSize >= 1) {
      setSubmitError("test_size must be a number between 0 and 1.");
      return;
    }

    setSubmitting(true);
    try {
      const hp = buildHyperparametersPayload({
        specs: selectedAlgorithm?.hyperparameter_specs,
        task,
        values: hyperparameters,
      });

      const payload = {
        dataset: Number(datasetId),
        algorithm: Number(algorithmId),
        hyperparameters: hp,
        test_size: testSize,
        random_state: randomState,
        include_predictions: includePredictions,
        include_probabilities: isClassification ? includeProbabilities : false,
      };

      const created = await createExperiment(payload);

      // MVP: go back to Home (experiments list)
      // Later: navigate(`/experiments/${created.id}`)
      navigate("/", { replace: true });
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        (typeof err?.response?.data === "string" ? err.response.data : null) ||
        "Failed to run experiment. Please check input and try again.";
      setSubmitError(msg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      {(errorMsg || submitError) && (
        <div className="rounded-xl border border-red-800/60 bg-red-950/40 p-4 text-red-200">
          {errorMsg || submitError}
        </div>
      )}

      {datasetsLoading ? (
        <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
          Loading datasets...
        </div>
      ) : (
        <DatasetPicker
          datasets={datasets}
          selectedId={datasetId}
          onSelect={setDatasetId}
        />
      )}

      {datasetId && (
        algorithmsLoading ? (
          <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
            Loading algorithms...
          </div>
        ) : (
          <AlgorithmPicker
            algorithms={filteredAlgorithms}
            selectedId={algorithmId}
            onSelect={setAlgorithmId}
          />
        )
      )}

      {datasetId && algorithmId && selectedAlgorithm && (
        <>
          <HyperparametersForm
            specs={selectedAlgorithm.hyperparameter_specs}
            task={task}
            values={hyperparameters}
            onChange={setHyperparameters}
          />

          {/* Split + output options (minimal UI for now) */}
          <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 space-y-4">
            <h2 className="text-xl font-bold text-white">Run configuration</h2>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="space-y-1">
                <label className="text-sm font-semibold text-slate-200">
                  Test size
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0.05"
                  max="0.95"
                  value={testSize}
                  onChange={(e) => setTestSize(Number(e.target.value))}
                  className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <p className="text-xs text-slate-400">
                  Fraction of data used for testing (0–1).
                </p>
              </div>

              <div className="space-y-1">
                <label className="text-sm font-semibold text-slate-200">
                  Random state
                </label>
                <input
                  type="number"
                  value={randomState}
                  onChange={(e) => setRandomState(Number(e.target.value))}
                  className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div className="flex flex-col gap-3">
              <label className="flex items-center gap-2 text-sm text-slate-200">
                <input
                  type="checkbox"
                  checked={includePredictions}
                  onChange={(e) => setIncludePredictions(e.target.checked)}
                />
                Include predictions in results
              </label>

              <label className="flex items-center gap-2 text-sm text-slate-200">
                <input
                  type="checkbox"
                  checked={includeProbabilities}
                  disabled={!isClassification}
                  onChange={(e) => setIncludeProbabilities(e.target.checked)}
                />
                Include probabilities (classification only)
              </label>
            </div>
          </section>

          {/* Run button */}
          <div className="flex items-center justify-end">
            <button
              type="button"
              onClick={handleRunExperiment}
              disabled={!canSubmit}
              className={[
                "rounded-xl px-5 py-3 text-sm font-semibold transition",
                canSubmit
                  ? "bg-emerald-600 text-white hover:bg-emerald-700 cursor-pointer"
                  : "bg-slate-700 text-slate-300 cursor-not-allowed",
              ].join(" ")}
            >
              {submitting ? "Running..." : "Run experiment"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
