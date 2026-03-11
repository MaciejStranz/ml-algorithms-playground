import DatasetCard from "./DatasetCard";
import { useDatasetsQuery } from "../../queries/datasets/useDatasetsQuery";
import LoadingCard from "../UI/LoadingCard";
import ErrorBanner from "../UI/ErrorBanner";
import EmptyState from "../UI/EmptyState";
import ResourceList from "../UI/ResourceList";

export default function DatasetsList() {
  const {data: datasets = [], isPending, error} = useDatasetsQuery();

  if (isPending) return <LoadingCard text="Loading datasets..." />;
  if (error) return <ErrorBanner message={error?.response?.data?.detail || "Failed to load datasets"} />;

  return (
    <div className="space-y-4">

      {datasets.length === 0 && (
        <EmptyState text="No datasets available." />
      )}

      {datasets.length > 0 && (
        <ResourceList
          items={datasets}
          renderItem={(d) => <DatasetCard key={d.id} dataset={d} />}
        />
      )}
    </div>
  );
}
