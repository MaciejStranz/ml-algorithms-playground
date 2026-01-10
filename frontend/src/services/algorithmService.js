import api from "../api";

export async function fetchAlgorithms({signal} = {}) {
    const res = await api.get("api/algorithms/", {signal});
    return res.data;
}