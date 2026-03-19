import { useQuery } from "@tanstack/react-query";
import { fetchExperiments } from "../../services/experimentService";
import { queryKeys } from "../../lib/queryKeys";


export function useExperimentsQuery() {
    return useQuery({
        queryKey: queryKeys.experiments,
        queryFn: ({signal}) => fetchExperiments({signal})
    })
}