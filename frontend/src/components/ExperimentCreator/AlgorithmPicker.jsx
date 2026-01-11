import AlgorithmSelectCard from "./AlgorithmSelectCard";

export default function AlgorithmPicker({ algorithms, selectedId, onSelect }) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-bold text-white">Choose algorithm</h2>
        <p className="mt-1 text-sm text-slate-300">
          Pick an algorithm compatible with the selected dataset task.
        </p>
      </div>

      <div className="space-y-4">
        {algorithms.map((a) => (
          <AlgorithmSelectCard
            key={a.id}
            algorithm={a}
            selected={String(a.id) === String(selectedId)}
            onSelect={onSelect}
          />
        ))}
      </div>
    </section>
  );
}
