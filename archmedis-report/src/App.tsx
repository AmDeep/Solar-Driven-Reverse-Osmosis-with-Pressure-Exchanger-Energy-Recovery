import { Switch, Route, Router as WouterRouter, Link, useLocation } from "wouter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/sonner";
import ReportPage from "@/pages/ReportPage";
import CADPage from "@/pages/CADPage";
import CFDPage from "@/pages/CFDPage";

const queryClient = new QueryClient();

function NavBar() {
  const [loc] = useLocation();
  const links = [
    { href: "/", label: "Engineering Report" },
    { href: "/cad", label: "CAD Concept" },
    { href: "/cfd", label: "CFD Study" },
  ];
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-slate-950/95 backdrop-blur border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded bg-cyan-500 flex items-center justify-center">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5">
              <path d="M12 2L2 7l10 5 10-5-10-5z" /><path d="M2 17l10 5 10-5" /><path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <span className="text-white font-semibold text-sm tracking-tight">Archmedis Technical Trial</span>
          <span className="text-slate-500 text-xs">Round 2 — Seawater-to-Freshwater Challenge</span>
        </div>
        <nav className="flex items-center gap-1">
          {links.map(l => (
            <Link key={l.href} href={l.href}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${loc === l.href ? "bg-cyan-500/20 text-cyan-400" : "text-slate-400 hover:text-white hover:bg-slate-800"}`}>
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}

function Router() {
  return (
    <Switch>
      <Route path="/" component={ReportPage} />
      <Route path="/cad" component={CADPage} />
      <Route path="/cfd" component={CFDPage} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, "")}>
        <div className="min-h-screen bg-slate-950 text-slate-100">
          <NavBar />
          <Router />
        </div>
        <Toaster />
      </WouterRouter>
    </QueryClientProvider>
  );
}

export default App;
