import { useQuery } from "@tanstack/react-query";
import { fetchExperimentById } from "../../services/experimentService";
import { queryKeys } from "../../lib/queryKeys";

export function useExperimentByIdQuery(experimentId) {
    return useQuery({
        queryKey: queryKeys.experimentById(experimentId),
        queryFn: () => fetchExperimentById(experimentId)
    });
}