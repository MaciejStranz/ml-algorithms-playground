import DatasetsList from "../components/Datasets/DatasetsList";

export default function Datasets() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 px-4 py-10">
      <div className="mx-auto w-full max-w-5xl space-y-6">
        <div>
          <h1 className="text-4xl font-extrabold text-white">Datasets</h1>
          <p className="mt-2 text-slate-300">
            Available datasets that can be used to run experiments.
          </p>
        </div>

        <DatasetsList />
      </div>
    </div>
  );
}
