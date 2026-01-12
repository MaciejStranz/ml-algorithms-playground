import api from "../api";

export async function fetchExperiments({signal} = {}) {
    const res = await api.get("api/experiments/", {signal});
    return res.data;
}

export async function deleteExperiment(id) {
    const res = await api.delete(`api/experiments/${id}/`);
}

export async function createExperiment(payload) {
  const res = await api.post("/api/experiments/", payload);
  return res.data;
}

export async function fetchExperimentById(id, { signal } = {}) {
  const res = await api.get(`/api/experiments/${id}/`, { signal });
  return res.data;
}

