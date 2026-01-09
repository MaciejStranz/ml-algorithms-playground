import { useMemo, useState } from "react";
import { fetchDatasets } from "../../services/datasetService";
import { useResourceList } from "../../hooks/useResourceList";
import DatasetPicker from "./DatasetPicker";

export default function ExperimentCreatorWizard() {
  const [datasetId, setDatasetId] = useState("");

  const {
    items: datasets,
    loading: datasetsLoading,
    errorMsg,
  } = useResourceList(
    ({ signal }) => fetchDatasets({ signal }),
    []
  );

  const selectedDataset = useMemo(
    () => datasets.find((d) => String(d.id) === String(datasetId)),
    [datasets, datasetId]
  );

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
        <DatasetPicker
          datasets={datasets}
          selectedId={datasetId}
          onSelect={setDatasetId}
        />
      )}

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
