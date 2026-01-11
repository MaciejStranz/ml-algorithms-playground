import { useMemo } from "react";

function coerceNumber(value, kind) {
  if (value === "" || value === null || value === undefined) return null;
  const n = Number(value);
  if (Number.isNaN(n)) return kind === "int" ? null : null;
  return kind === "int" ? Math.trunc(n) : n;
}

function safeStringify(val) {
  try {
    return JSON.stringify(val);
  } catch {
    return String(val);
  }
}

function FieldWrapper({ label, description, children }) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-semibold text-slate-200">{label}</label>
      {description && <p className="text-xs text-slate-400">{description}</p>}
      {children}
    </div>
  );
}

export default function HyperparametersForm({ specs, task, values, onChange }) {
  const applicableSpecs = useMemo(() => {
    const list = Array.isArray(specs) ? specs : [];
    if (!task) return list;

    return list.filter((s) => {
      const tasks = Array.isArray(s.applicable_tasks) ? s.applicable_tasks : [];
      return tasks.length === 0 || tasks.includes(task);
    });
  }, [specs, task]);

  const setValue = (name, value) => {
    onChange({ ...values, [name]: value });
  };

  return (
    <section className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 space-y-5">
      <div>
        <h2 className="text-xl font-bold text-white">Hyperparameters</h2>
        <p className="mt-1 text-sm text-slate-300">
          Configure hyperparameters for the selected algorithm.
        </p>
      </div>

      {applicableSpecs.length === 0 ? (
        <div className="rounded-xl bg-slate-950/40 p-4 text-slate-200">
          No hyperparameters available for this task.
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
          {applicableSpecs.map((spec) => {
            const name = spec.name;
            const label = spec.display_name || spec.name;
            const desc = spec.description;

            const current =
              values?.[name] !== undefined ? values[name] : spec.default;

            // --- BOOL
            if (spec.type === "bool") {
              return (
                <div key={name} className="rounded-xl bg-slate-950/40 p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="text-sm font-semibold text-slate-200">
                        {label}
                      </div>
                      {desc && (
                        <div className="mt-1 text-xs text-slate-400">{desc}</div>
                      )}
                    </div>

                    <input
                      type="checkbox"
                      checked={Boolean(current)}
                      onChange={(e) => setValue(name, e.target.checked)}
                    />
                  </div>
                </div>
              );
            }

            // --- CHOICE
            if (spec.type === "choice" && Array.isArray(spec.choices)) {
              return (
                <FieldWrapper key={name} label={label} description={desc}>
                  <select
                    className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={current ?? ""}
                    onChange={(e) => setValue(name, e.target.value)}
                  >
                    {spec.choices.map((c) => (
                      <option key={String(c)} value={c}>
                        {String(c)}
                      </option>
                    ))}
                  </select>
                </FieldWrapper>
              );
            }

            // --- INT_LIST (edytujemy jako JSON array)
            if (spec.type === "int_list") {
              return (
                <FieldWrapper key={name} label={label} description={desc}>
                  <input
                    className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 font-mono text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={Array.isArray(current) ? safeStringify(current) : (current ?? "[]")}
                    onChange={(e) => {
                      const raw = e.target.value;
                      try {
                        const parsed = JSON.parse(raw);
                        if (Array.isArray(parsed) && parsed.every((x) => Number.isInteger(x))) {
                          setValue(name, parsed);
                        } else {
                          // jeżeli niepoprawne, zostaw jako string (nie psuj stanu)
                          setValue(name, raw);
                        }
                      } catch {
                        setValue(name, raw);
                      }
                    }}
                    placeholder='[64, 64]'
                  />
                  <p className="text-xs text-slate-400">
                    Provide a JSON array of integers, e.g. <span className="font-mono">[64, 64]</span>
                  </p>
                </FieldWrapper>
              );
            }

            // --- NUMBER OR STRING
            if (spec.type === "number_or_string") {
              return (
                <FieldWrapper key={name} label={label} description={desc}>
                  <input
                    className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={current ?? ""}
                    onChange={(e) => setValue(name, e.target.value)}
                    placeholder={spec.default ?? ""}
                  />
                  {Array.isArray(spec.choices) && spec.choices.length > 0 && (
                    <p className="text-xs text-slate-400">
                      Allowed strings: {spec.choices.map(String).join(", ")} (or a numeric value)
                    </p>
                  )}
                </FieldWrapper>
              );
            }

            // --- INT / FLOAT
            if (spec.type === "int" || spec.type === "float") {
              return (
                <FieldWrapper key={name} label={label} description={desc}>
                  <input
                    className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    type="number"
                    step={spec.type === "int" ? 1 : "any"}
                    min={spec.min ?? undefined}
                    max={spec.max ?? undefined}
                    value={current ?? ""}
                    onChange={(e) => setValue(name, coerceNumber(e.target.value, spec.type))}
                  />
                </FieldWrapper>
              );
            }

            // --- fallback: string
            return (
              <FieldWrapper key={name} label={label} description={desc}>
                <input
                  className="w-full rounded-xl border border-slate-700 bg-slate-950/40 p-3 text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  value={current ?? ""}
                  onChange={(e) => setValue(name, e.target.value)}
                />
              </FieldWrapper>
            );
          })}
        </div>
      )}
    </section>
  );
}
