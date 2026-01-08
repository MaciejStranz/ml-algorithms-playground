import { useEffect, useState } from "react";

/**
 * Generic list loader hook.
 * - loader: ({ signal }) => Promise<data>
 * - supports DRF pagination and plain lists
 */
export function useResourceList(loader, deps = []) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      setLoading(true);
      setErrorMsg("");

      try {
        const data = await loader({ signal: controller.signal });

        const normalized = Array.isArray(data)
          ? data
          : Array.isArray(data?.results)
            ? data.results
            : [];

        setItems(normalized);
      } catch (err) {
        if (err?.code === "ERR_CANCELED") return;

        const msg =
          err?.response?.data?.detail ||
          "Failed to load data. Please try again.";
        setErrorMsg(msg);
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return { items, loading, errorMsg, setItems };
}