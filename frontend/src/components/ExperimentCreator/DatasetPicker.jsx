import DatasetSelectCard from "./DatasetSelectCard";

export default function DatasetPicker({ datasets, selectedId, onSelect }) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="text-xl font-bold text-white">Choose dataset</h2>
        <p className="mt-1 text-sm text-slate-300">
          Click a dataset card to select it.
        </p>
      </div>

      <div className="space-y-4">
        {datasets.map((ds) => (
          <DatasetSelectCard
            key={ds.id}
            dataset={ds}
            selected={String(ds.id) === String(selectedId)}
            onSelect={onSelect}
          />
        ))}
      </div>
    </section>
  );
}
