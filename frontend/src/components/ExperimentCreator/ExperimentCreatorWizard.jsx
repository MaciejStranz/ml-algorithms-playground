import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useDatasetsQuery } from "../../queries/datasets/useDatasetsQuery";
import { useAlgorithmVariantsQuery } from "../../queries/algorithms/useAlgorithmVariantsQuery";
import { useCreateExperimentMutation } from "../../queries/experiments/useCreateExperimentMutation";

import DatasetPicker from "./DatasetPicker";
import AlgorithmPicker from "./AlgorithmPicker";
import HyperparametersForm from "./HyperParametersForm";
import { buildHyperparametersPayload } from "../../utils/hyperparameters";

export default function ExperimentCreatorWizard() {
  const navigate = useNavigate();
  // user input
  const [datasetId, setDatasetId] = useState("");
  const [algorithmVariantId, setAlgorithmVariantId] = useState("");
  const [hyperparameters, setHyperparameters] = useState({});

  // config
  const [testSize, setTestSize] = useState(0.3);
  const [randomState, setRandomState] = useState(42);
  const [includePredictions, setIncludePredictions] = useState(true);
  const [includeProbabilities, setIncludeProbabilities] = useState(false);

  // submit state
  const [submitError, setSubmitError] = useState("");

  const createExperimentMutation = useCreateExperimentMutation();

  const {
    data: datasets = [],
    isPending: datasetsLoading,
    error: datasetsErrorObj,
  } = useDatasetsQuery();

  const selectedDataset = useMemo(
    () => datasets.find((d) => String(d.id) === String(datasetId)),
    [datasets, datasetId],
  );

  const task = selectedDataset?.task;

  const {
    data: algorithmVariants = [],
    isPending: algorithmVariantsLoading,
    error: algorithmVariantsErrorObj,
  } = useAlgorithmVariantsQuery(task);

  const selectedVariant = useMemo(
    () =>
      algorithmVariants.find(
        (v) => String(v.id) === String(algorithmVariantId),
      ),
    [algorithmVariants, algorithmVariantId],
  );

  const datasetsError = datasetsErrorObj?.response?.data?.detail || "";
  const algorithmsError =
    algorithmVariantsErrorObj?.response?.data?.detail || "";

  function getDefaultHyperparameters(specs) {
    const defaults = {};

    for (const spec of specs ?? []) {
      if (!spec?.name) continue;
      defaults[spec.name] = spec.default ?? null;
    }

    return defaults;
  }
  
  function handleDatasetSelect(nextDatasetId) {
    setDatasetId(nextDatasetId);
    setAlgorithmVariantId("");
    setHyperparameters({});
    setSubmitError("");
    setIncludeProbabilities(false);
  }

  function handleAlgorithmVariantSelect(nextVariantId) {
    setAlgorithmVariantId(nextVariantId);

    const nextVariant = algorithmVariants.find(
      (variant) => String(variant.id) === String(nextVariantId),
    );

    setHyperparameters(
      getDefaultHyperparameters(nextVariant?.hyperparameter_specs),
    );
    setSubmitError("");
  }

  const errorMsg = datasetsError || algorithmsError;

  const isClassification = task?.endsWith("_classification");
  const canSubmit =
    Boolean(datasetId) &&
    Boolean(algorithmVariantId) &&
    !datasetsLoading &&
    !algorithmVariantsLoading &&
    !createExperimentMutation.isPending;

  async function handleRunExperiment() {
    setSubmitError("");

    if (!datasetId || !algorithmVariantId) {
      setSubmitError("Please select dataset and algorithm first.");
      return;
    }

    // basic client-side validation (keep it light; backend is source of truth)
    if (typeof testSize !== "number" || testSize <= 0 || testSize >= 1) {
      setSubmitError("test_size must be a number between 0 and 1.");
      return;
    }

    try {
      const hp = buildHyperparametersPayload({
        specs: selectedVariant?.hyperparameter_specs,
        values: hyperparameters,
      });

      const payload = {
        dataset: Number(datasetId),
        algorithm_variant: Number(algorithmVariantId),
        hyperparameters: hp,
        test_size: testSize,
        random_state: randomState,
        include_predictions: includePredictions,
        include_probabilities: isClassification ? includeProbabilities : false,
      };

      await createExperimentMutation.mutateAsync(payload);

      // MVP: go back to Home (experiments list)
      // Later: navigate(`/experiments/${created.id}`)
      navigate("/", { replace: true });
      window.scrollTo({ top: 0, left: 0, behavior: "auto" });
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        (typeof err?.response?.data === "string" ? err.response.data : null) ||
        "Failed to run experiment. Please check input and try again.";
      setSubmitError(msg);
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
          onSelect={handleDatasetSelect}
        />
      )}

      {datasetId &&
        (algorithmVariantsLoading ? (
          <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
            Loading algorithms...
          </div>
        ) : (
          <AlgorithmPicker
            algorithmVariants={algorithmVariants}
            selectedId={algorithmVariantId}
            onSelect={handleAlgorithmVariantSelect}
          />
        ))}

      {datasetId && algorithmVariantId && selectedVariant && (
        <>
          <HyperparametersForm
            specs={selectedVariant.hyperparameter_specs}
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
              {createExperimentMutation.isPending
                ? "Running..."
                : "Run experiment"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
