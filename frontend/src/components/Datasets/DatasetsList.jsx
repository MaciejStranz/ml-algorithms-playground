import DatasetCard from "./DatasetCard";
import { fetchDatasets } from "../../services/datasetService";
import { useResourceList } from "../../hooks/useResourceList";
import LoadingCard from "../UI/LoadingCard";
import ErrorBanner from "../UI/ErrorBanner";
import EmptyState from "../UI/EmptyState";
import ResourceList from "../UI/ResourceList";

export default function DatasetsList() {
  const { items: datasets, loading, errorMsg } = useResourceList(
    ({ signal }) => fetchDatasets({ signal }),
    []
  );

  if (loading) return <LoadingCard text="Loading datasets..." />;

  return (
    <div className="space-y-4">
      <ErrorBanner message={errorMsg} />

      {!errorMsg && datasets.length === 0 && (
        <EmptyState text="No datasets available." />
      )}

      {!errorMsg && datasets.length > 0 && (
        <ResourceList
          items={datasets}
          renderItem={(d) => <DatasetCard key={d.id} dataset={d} />}
        />
      )}
    </div>
  );
}
