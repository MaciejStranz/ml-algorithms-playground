import api from "../api";

export async function fetchDatasets({signal} = {}) {
    const res = await api.get("api/datasets/", {signal});
    return res.data;
}