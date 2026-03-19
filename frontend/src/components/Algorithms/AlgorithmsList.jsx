import { useAlgorithmsQuery } from "../../queries/algorithms/useAlgorithmsQuery";

import LoadingCard from "../UI/LoadingCard";
import ErrorBanner from "../UI/ErrorBanner";
import EmptyState from "../UI/EmptyState";
import ResourceList from "../UI/ResourceList";

import AlgorithmCard from "./AlgorithmCard";

export default function AlgorithmsList() {
  const {data: algorithms = [], isPending, error} = useAlgorithmsQuery();

  if (isPending) return <LoadingCard text="Loading algorithms..." />;
  if (error) return <ErrorBanner message={error?.response?.data?.detail || "Failed to load algorithms"} />;

  return (
    <div className="space-y-4">

      {algorithms.length === 0 && (
        <EmptyState text="No algorithms available." />
      )}

      {algorithms.length > 0 && (
        <ResourceList
          items={algorithms}
          renderItem={(a) => <AlgorithmCard key={a.id} algorithm={a} />}
        />
      )}
    </div>
  );
}
