import StatusPill from "@/components/StatusPill";
import { getHealth } from "@/lib/api";

export default async function Status() {
  let ok = false;
  try {
    const res = await getHealth();
    ok = res.status === "ok";
  } catch {
    ok = false;
  }
  return (
    <div className="card flex items-center justify-between">
      <div>
        <div className="h2">System status</div>
        <div className="small">Backend API: <code>/api/health</code></div>
      </div>
      <StatusPill ok={ok} />
    </div>
  );
}
