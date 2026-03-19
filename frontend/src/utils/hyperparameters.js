function isNumberString(s) {
  if (typeof s !== "string") return false;
  if (s.trim() === "") return false;
  return !Number.isNaN(Number(s));
}

export function buildHyperparametersPayload({ specs, values }) {
  const hyperparamSpecs = Array.isArray(specs) ? specs : [];
  const out = {};

  for (const spec of hyperparamSpecs) {
    const name = spec?.name;
    if (!name) continue;

    const raw = values?.[name];

    // If user never touched the field, prefer default
    const value = raw !== undefined ? raw : spec.default;

    if (spec.type === "int_list") {
      if (Array.isArray(value)) {
        out[name] = value;
        continue;
      }
      if (typeof value === "string") {
        try {
          const parsed = JSON.parse(value);
          if (Array.isArray(parsed) && parsed.every(Number.isInteger)) {
            out[name] = parsed;
            continue;
          }
        } catch {
          // fallthrough
        }
      }
      // invalid -> let backend validate OR omit
      out[name] = value;
      continue;
    }

    if (spec.type === "number_or_string") {
      if (typeof value === "string" && isNumberString(value)) {
        out[name] = Number(value);
      } else {
        out[name] = value;
      }
      continue;
    }

    out[name] = value;
  }

  return out;
}
