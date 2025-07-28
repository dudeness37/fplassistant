type Mark = { gw: number; label?: string; type?: "WC" | "BB" | "FH" | "TC" };

export default function Timeline({ start=1, end=18, marks=[] }: { start?: number; end?: number; marks?: Mark[] }) {
  const total = end - start + 1;
  return (
    <div className="w-full card">
      <div className="h-2 bg-slate-800 rounded-full relative">
        {marks.map((m, i) => {
          const pct = ((m.gw - start) / (total - 1)) * 100;
          return (
            <div key={i} className="absolute -top-2" style={{ left: `${pct}%` }}>
              <div className="h-4 w-4 bg-blue-400 rounded-full border-2 border-slate-900" title={`${m.type || ""} GW${m.gw} ${m.label || ""}`} />
              <div className="text-[10px] text-slate-300 mt-1 -translate-x-1/2 text-center">GW{m.gw}{m.type?` · ${m.type}`:""}</div>
            </div>
          );
        })}
      </div>
      <div className="flex justify-between text-[10px] text-slate-400 mt-2">
        <span>GW{start}</span>
        <span>GW{end}</span>
      </div>
    </div>
  );
}
