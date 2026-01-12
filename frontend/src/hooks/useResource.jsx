import { useEffect, useState } from "react";

export function useResource(loader, deps = [], options = {}) {
  const { fallbackErrorMessage = "Failed to load data. Please try again." } = options;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      setLoading(true);
      setErrorMsg("");

      try {
        const result = await loader({ signal: controller.signal });
        setData(result);
      } catch (err) {
        if (err?.code === "ERR_CANCELED") return;

        const msg = err?.response?.data?.detail || fallbackErrorMessage;
        setErrorMsg(msg);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, deps);

  return { data, loading, errorMsg, setData };
}