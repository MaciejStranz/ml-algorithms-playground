export default function ResourceList({ items, renderItem }) {
  return <div className="space-y-4">{items.map(renderItem)}</div>;
}
