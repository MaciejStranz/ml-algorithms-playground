import { useQuery } from "@tanstack/react-query";
import { fetchAlgorithms } from "../../services/algorithmService";
import { queryKeys } from "../../lib/queryKeys";

export function useAlgorithmsQuery() {
    return useQuery({
        queryKey: queryKeys.algorithms,
        queryFn: ({signal}) => fetchAlgorithms({signal})
    })
}