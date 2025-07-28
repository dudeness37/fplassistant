import Link from "next/link";

export default function Nav() {
  return (
    <header className="w-full border-b border-slate-800 bg-slate-900/50 backdrop-blur">
      <div className="mx-auto max-w-6xl px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="text-lg font-semibold">FPL AI</Link>
          <nav className="hidden md:flex gap-4 text-sm">
            <Link href="/preseason" className="hover:underline">Preseason Wizard</Link>
            <Link href="/chips" className="hover:underline">Chip Planner</Link>
            <Link href="/squad" className="hover:underline">Squad</Link>
            <Link href="/watchlist" className="hover:underline">Watchlist</Link>
            <Link href="/settings" className="hover:underline">Settings</Link>
          </nav>
        </div>
        <div className="text-xs text-slate-400">25/26</div>
      </div>
    </header>
  );
}
