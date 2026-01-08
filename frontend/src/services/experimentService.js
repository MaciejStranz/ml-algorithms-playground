import api from "../api";

export async function fetchExperiments({signal} = {}) {
    const res = await api.get("api/experiments/", {signal});
    return res.data;
}

export async function deleteExperiment(id) {
    const res = await api.delete(`api/experiments/${id}/`);
}