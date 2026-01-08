import { useEffect, useMemo, useState } from "react";
import { fetchDatasets } from "../../services/datasetService";
import DatasetSelect from "./DatasetSelect";

export default function ExperimentCreatorWizard() {
  const [datasets, setDatasets] = useState([]);
  const [datasetsLoading, setDatasetsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  const [datasetId, setDatasetId] = useState("");

  const selectedDataset = useMemo(
    () => datasets.find((d) => String(d.id) === String(datasetId)),
    [datasets, datasetId]
  );

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      setDatasetsLoading(true);
      setErrorMsg("");

      try {
        const data = await fetchDatasets({ signal: controller.signal });
        const items = Array.isArray(data) ? data : (data?.results ?? []);
        setDatasets(items);
      } catch (err) {
        if (err?.code === "ERR_CANCELED") return;
        const msg =
          err?.response?.data?.detail ||
          "Failed to load datasets. Please try again.";
        setErrorMsg(msg);
      } finally {
        setDatasetsLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, []);

  return (
    <div className="space-y-6">
      {errorMsg && (
        <div className="rounded-xl border border-red-800/60 bg-red-950/40 p-4 text-red-200">
          {errorMsg}
        </div>
      )}

      {datasetsLoading ? (
        <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
          Loading datasets...
        </div>
      ) : (
        <DatasetSelect
          datasets={datasets}
          value={datasetId}
          onChange={setDatasetId}
        />
      )}

      {/* Debug / placeholder for next step */}
      <div className="rounded-2xl border border-slate-700 bg-slate-900/40 p-6 text-slate-200">
        <div className="text-sm text-slate-400">Next step</div>
        <div className="mt-1">
          Selected dataset:{" "}
          <span className="font-semibold text-white">
            {selectedDataset?.name ?? "—"}
          </span>
        </div>
        <div className="mt-1">
          Task:{" "}
          <span className="font-semibold text-white">
            {selectedDataset?.task ?? "—"}
          </span>
        </div>
      </div>
    </div>
  );
}
