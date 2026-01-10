import AlgorithmsList from "../components/Algorithms/AlgorithmsList";

export default function Algorithms() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 px-4 py-10">
      <div className="mx-auto w-full max-w-5xl space-y-6">
        <div>
          <h1 className="text-4xl font-extrabold text-white">Algorithms</h1>
          <p className="mt-2 text-slate-300">
            Available algorithms and their hyperparameter configuration options.
          </p>
        </div>

        <AlgorithmsList />
      </div>
    </div>
  );
}
