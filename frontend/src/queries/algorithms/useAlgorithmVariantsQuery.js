import { useQuery } from "@tanstack/react-query";
import { fetchAlgorithmVariantsByTask } from "../../services/algorithmVariantService";
import { queryKeys } from "../../lib/queryKeys";

export function useAlgorithmVariantsQuery(task) {
    return useQuery({
        queryKey: queryKeys.algorithmVariants(task),
        queryFn: ({signal}) => fetchAlgorithmVariantsByTask(task, {signal}), 
        enabled: Boolean(task),
    });
}