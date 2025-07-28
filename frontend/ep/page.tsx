export default async function EPTop() {
    const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
    const res = await fetch(`${base}/api/ep/top?gw=1&limit=20`, { cache: "no-store" });
    const data = await res.json();
  
    return (
      <div className="space-y-4">
        <h1 className="text-2xl font-bold">Top EP (GW1)</h1>
        <div className="card overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-slate-400">
                <th className="py-2 pr-4">Player</th>
                <th className="py-2 pr-4">Pos</th>
                <th className="py-2 pr-4">Team</th>
                <th className="py-2 pr-4">Cost</th>
                <th className="py-2 pr-4">EP</th>
              </tr>
            </thead>
            <tbody>
              {data.map((r: any, i: number) => (
                <tr key={i} className="border-t border-slate-800">
                  <td className="py-2 pr-4">{r.web_name}</td>
                  <td className="py-2 pr-4">{r.pos}</td>
                  <td className="py-2 pr-4">{r.team_id}</td>
                  <td className="py-2 pr-4">{r.cost.toFixed(1)}m</td>
                  <td className="py-2 pr-4">{r.ep.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }
  