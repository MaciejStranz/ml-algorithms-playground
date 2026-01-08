export default function LoadingCard({ text = "Loading..." }) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900/60 p-6 text-slate-200">
      {text}
    </div>
  );
}