import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteExperiment } from "../../services/experimentService";
import { queryKeys } from "../../lib/queryKeys";

export function useDeleteExperimentMutation() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: deleteExperiment, 
        onSuccess: () => {queryClient.invalidateQueries({queryKey: queryKeys.experiments})},
    });
}