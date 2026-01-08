export default function ErrorBanner({ message }) {
  if (!message) return null;

  return (
    <div className="rounded-xl border border-red-800/60 bg-red-950/40 p-4 text-red-200">
      {message}
    </div>
  );
}
