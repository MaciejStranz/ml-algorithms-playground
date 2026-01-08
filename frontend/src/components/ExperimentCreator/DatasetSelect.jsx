export default function DatasetSelect({ datasets, value, onChange }) {
  const selected = datasets.find((d) => String(d.id) === String(value));

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white">1) Choose dataset</h2>
          <p className="mt-1 text-sm text-slate-300">
            Select a dataset to define the experiment task type.
          </p>
        </div>

        {selected?.task && (
          <span className="rounded-lg bg-slate-800 px-3 py-1 text-sm font-semibold text-slate-200">
            Task: {selected.task}
          </span>
        )}
      </div>

      <div className="mt-5">
        <label className="text-sm font-semibold text-slate-200">Dataset</label>
        <select
          className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        >
          <option value="">Select dataset...</option>
          {datasets.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>

        {selected && (
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="rounded-xl bg-slate-950/40 p-4">
              <div className="text-xs text-slate-400">Dataset</div>
              <div className="mt-1 text-sm font-medium text-slate-200">
                {selected.name}
              </div>
            </div>
            <div className="rounded-xl bg-slate-950/40 p-4">
              <div className="text-xs text-slate-400">Task</div>
              <div className="mt-1 text-sm font-medium text-slate-200">
                {selected.task ?? "—"}
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
