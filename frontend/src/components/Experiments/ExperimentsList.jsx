import ExperimentCard from "./ExperimentCard";
import { useExperimentsQuery } from "../../queries/experiments/useExperimentsQuery";
import { useDeleteExperimentMutation } from "../../queries/experiments/useDeleteExperimentMutation";
import LoadingCard from "../UI/LoadingCard";
import ErrorBanner from "../UI/ErrorBanner";
import EmptyState from "../UI/EmptyState";

export default function ExperimentsList() {
  const { data: experiments = [], isPending, error } = useExperimentsQuery();

  const deleteExperimentMutation = useDeleteExperimentMutation();

  const handleDelete = async (experiment) => {
    const ok = window.confirm(
      `Delete experiment #${experiment.id}? This cannot be undone.`,
    );
    if (!ok) return;

    deleteExperimentMutation.mutate(experiment.id);
  };

  const deleteErrorMessage =
    deleteExperimentMutation.error?.response?.data?.detail ||
    "Failed to delete experiment. Please try again.";

  if (isPending) return <LoadingCard text="Loading experiments..." />;
  if (error)
    return (
      <ErrorBanner
        message={error?.response?.data?.detail || "Failed to load experiments"}
      />
    );

  return (
    <div className="space-y-4">
      {deleteExperimentMutation.isError && (
        <ErrorBanner message={deleteErrorMessage} />
      )}

      {experiments.length === 0 ? (
        <EmptyState text="No experiments yet." />
      ) : (
        experiments.map((exp) => (
          <ExperimentCard
            key={exp.id}
            experiment={exp}
            onDelete={handleDelete}
            deleting={
              deleteExperimentMutation.isPending &&
              deleteExperimentMutation.variables === exp.id
            }
          />
        ))
      )}
    </div>
  );
}
