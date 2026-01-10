import { useCallback } from "react";
import { fetchAlgorithms } from "../../services/algorithmService";
import { useResourceList } from "../../hooks/useResourceList";

import LoadingCard from "../UI/LoadingCard";
import ErrorBanner from "../UI/ErrorBanner";
import EmptyState from "../UI/EmptyState";
import ResourceList from "../UI/ResourceList";

import AlgorithmCard from "./AlgorithmCard";

export default function AlgorithmsList() {
  const loader = useCallback(({ signal }) => fetchAlgorithms({ signal }), []);

  const { items: algorithms, loading, errorMsg } = useResourceList(
    loader,
    [loader],
    { fallbackErrorMessage: "Failed to load algorithms." }
  );

  if (loading) return <LoadingCard text="Loading algorithms..." />;

  return (
    <div className="space-y-4">
      <ErrorBanner message={errorMsg} />

      {!errorMsg && algorithms.length === 0 && (
        <EmptyState text="No algorithms available." />
      )}

      {!errorMsg && algorithms.length > 0 && (
        <ResourceList
          items={algorithms}
          renderItem={(a) => <AlgorithmCard key={a.id} algorithm={a} />}
        />
      )}
    </div>
  );
}
