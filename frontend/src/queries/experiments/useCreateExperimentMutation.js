import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createExperiment } from "../../services/experimentService";
import { queryKeys } from "../../lib/queryKeys";

export function useCreateExperimentMutation() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: createExperiment,
        onSuccess: () => queryClient.invalidateQueries({queryKey: queryKeys.experiments})
    });
}