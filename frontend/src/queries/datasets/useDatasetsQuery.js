import { useQuery } from "@tanstack/react-query";
import { fetchDatasets } from "../../services/datasetService";
import { queryKeys } from "../../lib/queryKeys";

export function useDatasetsQuery() {
    return useQuery({
        queryKey: queryKeys.datasets, 
        queryFn: ({signal}) => fetchDatasets({signal})
    })
}