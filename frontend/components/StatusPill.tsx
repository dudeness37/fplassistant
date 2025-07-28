export default function StatusPill({ ok }: { ok: boolean }) {
  return (
    <span className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs ${ok ? "bg-emerald-900/40 text-emerald-300" : "bg-rose-900/40 text-rose-300"}`}>
      <span className={`h-2 w-2 rounded-full ${ok ? "bg-emerald-400" : "bg-rose-400"}`} />
      {ok ? "API: OK" : "API: DOWN"}
    </span>
  );
}
