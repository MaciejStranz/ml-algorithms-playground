import api from "../api";

export async function fetchAlgorithmVariantsByTask(task, {signal} = {}) {
    const res = await api.get("api/algorithm-variants/", {
        signal, 
        params: { task }
    });
    return res.data;
}