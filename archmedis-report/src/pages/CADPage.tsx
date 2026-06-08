import { useState } from "react";
import { PHYSICS } from "@/physics/constants";

// ─── Isometric helpers ────────────────────────────────────────────────────
// Classic 2:1 isometric projection
// iso(x, y, z) → screen (sx, sy)
// x = right, y = up, z = depth
function iso(x: number, y: number, z: number, ox = 0, oy = 0, scale = 1): [number, number] {
  const sx = (x - z) * Math.cos(Math.PI / 6) * scale + ox;
  const sy = -(y) * scale + (x + z) * Math.sin(Math.PI / 6) * scale + oy;
  return [sx, sy];
}

// Draw an isometric box (top + left + right faces)
function IsoBox({
  x, y, z, w, h, d, topFill, leftFill, rightFill, stroke = "#1e293b", strokeWidth = 0.8,
}: {
  x: number; y: number; z: number;
  w: number; h: number; d: number;
  topFill: string; leftFill: string; rightFill: string;
  stroke?: string; strokeWidth?: number;
}) {
  const ox = 400; const oy = 220; const sc = 55;

  const [bx, by] = iso(x, y, z, ox, oy, sc);
  const [bxw, byw] = iso(x + w, y, z, ox, oy, sc);
  const [bxwz, bywz] = iso(x + w, y, z + d, ox, oy, sc);
  const [bxz, byz] = iso(x, y, z + d, ox, oy, sc);

  const [tx, ty] = iso(x, y + h, z, ox, oy, sc);
  const [txw, tyw] = iso(x + w, y + h, z, ox, oy, sc);
  const [txwz, tywz] = iso(x + w, y + h, z + d, ox, oy, sc);
  const [txz, tyz] = iso(x, y + h, z + d, ox, oy, sc);

  const top = `M${tx},${ty} L${txw},${tyw} L${txwz},${tywz} L${txz},${tyz} Z`;
  const left = `M${tx},${ty} L${txz},${tyz} L${bxz},${byz} L${bx},${by} Z`;
  const right = `M${txw},${tyw} L${txwz},${tywz} L${bxwz},${bywz} L${bxw},${byw} Z`;
  const front = `M${tx},${ty} L${txw},${tyw} L${bxw},${byw} L${bx},${by} Z`;

  return (
    <g>
      <path d={left} fill={leftFill} stroke={stroke} strokeWidth={strokeWidth} />
      <path d={right} fill={rightFill} stroke={stroke} strokeWidth={strokeWidth} />
      <path d={top} fill={topFill} stroke={stroke} strokeWidth={strokeWidth} />
    </g>
  );
}

// Isometric cylinder (approximate with box + ellipse top)
function IsoCylinder({
  cx, cy, cz, r, h, topFill, sideFill,
}: {
  cx: number; cy: number; cz: number; r: number; h: number;
  topFill: string; sideFill: string;
}) {
  return (
    <IsoBox x={cx - r} y={cy} z={cz - r} w={r * 2} h={h} d={r * 2}
      topFill={topFill} leftFill={sideFill} rightFill={`${sideFill}cc`} />
  );
}

// Dimension line helper
function DimLine({ x1, y1, x2, y2, label, ox = 400, oy = 220, sc = 55 }: {
  x1: number; y1: number; x2: number; y2: number;
  label: string; ox?: number; oy?: number; sc?: number;
}) {
  const [sx1, sy1] = iso(x1, y1, 0, ox, oy, sc);
  const [sx2, sy2] = iso(x2, y2, 0, ox, oy, sc);
  const mx = (sx1 + sx2) / 2;
  const my = (sy1 + sy2) / 2 - 8;
  return (
    <g>
      <line x1={sx1} y1={sy1} x2={sx2} y2={sy2} stroke="#374151" strokeWidth="0.8" strokeDasharray="3 2" />
      <text x={mx} y={my} textAnchor="middle" fill="#64748b" fontSize="7">{label}</text>
    </g>
  );
}

// Flow arrow along iso line
function IsoArrow({ from, to, color, ox = 400, oy = 220, sc = 55 }: {
  from: [number, number, number]; to: [number, number, number];
  color: string; ox?: number; oy?: number; sc?: number;
}) {
  const [x1, y1] = iso(...from, ox, oy, sc);
  const [x2, y2] = iso(...to, ox, oy, sc);
  const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
  return (
    <g>
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={1.8}
        strokeDasharray={color === "#fbbf24" ? "4 3" : undefined} />
      <polygon
        points="-5,-3 5,0 -5,3"
        fill={color}
        transform={`translate(${x2},${y2}) rotate(${angle})`}
      />
    </g>
  );
}

export default function CADPage() {
  const [activeView, setActiveView] = useState<"iso" | "top" | "front" | "pid">("iso");
  const [showDimensions, setShowDimensions] = useState(true);
  const [showFlow, setShowFlow] = useState(true);

  return (
    <div className="pt-20 pb-24 max-w-6xl mx-auto px-6">
      <div className="mb-8 py-10 border-b border-slate-800">
        <div className="section-label">Deliverable 2 — CAD Concept</div>
        <h1 className="text-3xl font-black text-white mb-3">
          3D System Model — Solar SPRO Skid
        </h1>
        <p className="text-slate-400 text-sm max-w-2xl">
          Isometric concept drawings with principal dimensions. All components shown at correct
          relative scale inside a 40 ft ISO container (12.19 × 2.44 m).
          Switch between isometric, top, front views and the P&ID.
        </p>
      </div>

      {/* View controls */}
      <div className="flex items-center gap-2 mb-4">
        {(["iso", "top", "front", "pid"] as const).map(v => (
          <button key={v} onClick={() => setActiveView(v)}
            className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${activeView === v ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/40" : "text-slate-400 border border-slate-800 hover:bg-slate-800"}`}>
            {v === "iso" ? "Isometric" : v === "top" ? "Plan (Top)" : v === "front" ? "Elevation (Front)" : "P&ID"}
          </button>
        ))}
        <div className="ml-auto flex gap-2">
          <button onClick={() => setShowDimensions(!showDimensions)}
            className={`px-3 py-1 rounded text-xs transition-colors ${showDimensions ? "bg-slate-700 text-white" : "text-slate-500 border border-slate-800"}`}>
            Dimensions
          </button>
          <button onClick={() => setShowFlow(!showFlow)}
            className={`px-3 py-1 rounded text-xs transition-colors ${showFlow ? "bg-slate-700 text-white" : "text-slate-500 border border-slate-800"}`}>
            Flow paths
          </button>
        </div>
      </div>

      {/* Drawing area */}
      <div className="rounded-xl border border-slate-800 bg-slate-950 overflow-hidden mb-8">
        <div className="flex items-center gap-3 px-4 py-2 border-b border-slate-800 bg-slate-900">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-red-500/50" />
            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/50" />
            <div className="w-2.5 h-2.5 rounded-full bg-green-500/50" />
          </div>
          <span className="text-xs text-slate-500 font-mono">
            {activeView === "iso" ? "VIEW_ISOMETRIC.svg" : activeView === "top" ? "VIEW_PLAN.svg" : activeView === "front" ? "VIEW_ELEVATION.svg" : "PID_SHEET_01.svg"}
            {" — "} Solar SPRO System, 20,000 L/day  | Scale: NTS
          </span>
        </div>

        {activeView === "iso" && <IsometricView showDimensions={showDimensions} showFlow={showFlow} />}
        {activeView === "top" && <TopView showDimensions={showDimensions} showFlow={showFlow} />}
        {activeView === "front" && <FrontView showDimensions={showDimensions} />}
        {activeView === "pid" && <PIDView showFlow={showFlow} />}
      </div>

      {/* Legend */}
      <div className="grid grid-cols-4 gap-3 mb-10">
        {[
          { color: "#06b6d4", label: "Seawater / recovered feed", detail: "44.4 m³/day, 35 g/L → 60 bar" },
          { color: "#22c55e", label: "Permeate (freshwater)", detail: "20,000 L/day < 500 ppm TDS" },
          { color: "#f59e0b", label: "Brine reject", detail: "24,400 L/day at 63.6 g/L" },
          { color: "#fbbf24", label: "DC electrical", detail: "PV → battery → HP pump" },
        ].map((item, i) => (
          <div key={i} className="rounded-lg border border-slate-800 bg-slate-900/60 p-3 flex gap-3">
            <div className="w-3 h-3 rounded-full mt-0.5 shrink-0" style={{ background: item.color }} />
            <div>
              <div className="text-xs text-white font-medium">{item.label}</div>
              <div className="text-xs text-slate-500 mt-0.5">{item.detail}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Bill of Materials */}
      <section className="mb-10">
        <h2 className="text-lg font-bold text-white mb-4">Principal Dimensions & Bill of Materials</h2>
        <div className="rounded-xl border border-slate-800 overflow-hidden">
          <table className="w-full data-table">
            <thead>
              <tr>
                <th>Ref</th>
                <th>Component</th>
                <th>Model / Spec</th>
                <th>Key Dimensions</th>
                <th>Qty</th>
                <th>Material</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody className="text-slate-300">
              {[
                ["V-01", "RO pressure vessel", "Codeline 80S-6 (8\" × 6-element)", "L = 6.3 m, OD = 225 mm", "1", "FRP (filament-wound)", "PN 80 bar, end-entry"],
                ["ME-01–06", "RO membrane element", "Filmtec SW30XHR-400i", "L = 1016 mm, OD = 201 mm", "6", "Polyamide TFC on PS", "99.75% NaCl rejection"],
                ["P-01", "LP feed pump", "Grundfos CM5-6", "H = 260 mm, W = 140 mm", "1", "316L SS wetted parts", "2.5 bar, 3.0 m³/h"],
                ["P-02", "HP centrifugal pump", "Grundfos MTRE 45-3/5", "H = 420 mm, W = 200 mm", "1", "Duplex SS 2205", "60 bar, 1.85 m³/h, 5.5 kW"],
                ["E-01", "Pressure exchanger", "ERI PX-70 (or Danfoss APP 1.5)", "220 × 180 × 180 mm", "1", "Alumina ceramic rotor", "η = 96%, isobaric"],
                ["F-01", "UF pre-treatment", "Dow FilmTec Integrity 40–500", "L = 1.2 m, OD = 150 mm", "1", "PVDF hollow-fibre", "SDI < 3, 0.02 μm cutoff"],
                ["PV-01", "Solar panel", "Jinko Tiger NEO 400W N-type", "1722 × 1134 × 30 mm", "37", "Mono-Si, glass-glass", "21% STC, 25yr wty"],
                ["BAT-01", "LFP battery bank", "CATL 280 Ah prismatic", "173 × 71 × 207 mm / cell", "~48 cells", "LiFePO₄", "87.5 kWh at 48V system"],
                ["INV-01", "Inverter / MPPT", "Victron Quattro 48/8000", "446 × 265 × 192 mm", "1", "Aluminium housing", "8 kW AC, MPPT 150V/100A"],
                ["D-01", "Antiscalant dosing", "ProMinent CONCEPT plus", "300 × 200 × 100 mm", "1", "PP housing", "Genesys SW, < 5 ppm dose"],
                ["SKID", "Process skid", "Custom 316L SS tube frame", "2400 × 800 × 1800 mm", "1", "316L SS square tube", "Holds V-01, P-01/02, E-01, F-01"],
                ["CNT", "Enclosure", "ISO 40 ft container (modified)", "12,192 × 2438 × 2591 mm", "1", "Corten steel, zinc primer", "Houses skid + battery + inverter"],
              ].map(([ref, comp, model, dims, qty, mat, notes], i) => (
                <tr key={i}>
                  <td><code className="text-cyan-400 text-xs">{ref}</code></td>
                  <td className="font-medium text-white">{comp}</td>
                  <td className="text-slate-400 text-xs">{model}</td>
                  <td className="font-mono text-xs text-cyan-300">{dims}</td>
                  <td className="text-center">{qty}</td>
                  <td className="text-slate-500 text-xs">{mat}</td>
                  <td className="text-slate-500 text-xs">{notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Notes on design choices */}
      <section>
        <h2 className="text-lg font-bold text-white mb-3">Buildability & Volume Manufacturing Notes</h2>
        <div className="grid grid-cols-3 gap-4 text-sm">
          {[
            {
              title: "Containerised skid design",
              body: "All process components fit within a 40 ft ISO container (12.19 × 2.44 × 2.59 m). The 6.5 m RO vessel zone occupies the central 54% of length. Zones: A (pre-treatment, 0–2 m), B (HP pump + PX, 2–4.5 m), C (RO vessel, 4.5–11 m), D (permeate storage, 11–12.19 m). Battery bank runs the full top zone. No site building required.",
            },
            {
              title: "Modular linear scaling",
              body: "Output scales by adding vessel strings in parallel. 2 vessels → 40,000 L/day; 5 vessels → 100,000 L/day. All high-pressure connections use standard ½\" and ¾\" Victaulic couplings rated to 80 bar — no site welding. One shipping container = one autonomous module.",
            },
            {
              title: "Volume manufacturing path",
              body: "At 50+ units: BOM cost falls 25–35%. PV panels at $0.25/W, LFP cells at $80–100/kWh by 2026. HP pump and RO vessel dominate variable BOM. Factory flow: skid pre-wired + piped at workshop → container integration → ship. Site commissioning in < 3 days.",
            },
          ].map((item, i) => (
            <div key={i} className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
              <h4 className="text-white text-sm font-semibold mb-2">{item.title}</h4>
              <p className="text-slate-400 text-xs">{item.body}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

// ─── ISOMETRIC VIEW ────────────────────────────────────────────────────────
function IsometricView({ showDimensions, showFlow }: { showDimensions: boolean; showFlow: boolean }) {
  const ox = 400; const oy = 230; const sc = 52;

  return (
    <svg viewBox="0 0 800 480" className="w-full bg-slate-950">
      <defs>
        <pattern id="isoGrid" patternUnits="userSpaceOnUse" width="55" height="31.75"
          patternTransform={`translate(${ox},${oy})`}>
        </pattern>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>

      {/* Ground plane grid */}
      {Array.from({ length: 12 }, (_, i) => {
        const [x1, y1] = iso(-1, 0, i * 0.5 - 1, ox, oy, sc);
        const [x2, y2] = iso(7, 0, i * 0.5 - 1, ox, oy, sc);
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#0f172a" strokeWidth="0.5" />;
      })}
      {Array.from({ length: 16 }, (_, i) => {
        const [x1, y1] = iso(i * 0.5 - 1, 0, -1, ox, oy, sc);
        const [x2, y2] = iso(i * 0.5 - 1, 0, 5, ox, oy, sc);
        return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#0f172a" strokeWidth="0.5" />;
      })}

      {/* Container outline (40 ft = 12.19 m) — scaled to 6 units wide */}
      <IsoBox x={-0.2} y={-0.05} z={-0.2} w={6.4} h={0.05} d={2.6}
        topFill="#0c1a2e" leftFill="#091422" rightFill="#091422" stroke="#1e3a5f" strokeWidth={1.2} />
      {/* Container walls */}
      <IsoBox x={-0.2} y={0} z={-0.2} w={0.05} h={2.4} d={2.6}
        topFill="#0a1628" leftFill="#0a1628" rightFill="#0a1628" stroke="#1e3a5f" strokeWidth={0.8} />
      <IsoBox x={6.15} y={0} z={-0.2} w={0.05} h={2.4} d={2.6}
        topFill="#0a1628" leftFill="#0a1628" rightFill="#0a1628" stroke="#1e3a5f" strokeWidth={0.8} />

      {/* Container label */}
      {(() => { const [sx, sy] = iso(3, 2.5, 1.0, ox, oy, sc); return (
        <text x={sx} y={sy - 5} textAnchor="middle" fill="#1e3a5f" fontSize="9" fontWeight="600">
          ISO 40 ft CONTAINER (12.19 × 2.44 × 2.59 m)
        </text>
      ); })()}

      {/* Solar array on roof */}
      {[0, 1, 2, 3].map(row => [0, 1, 2, 3, 4, 5, 6].map(col => (
        <IsoBox key={`${row}-${col}`}
          x={0.2 + col * 0.82} y={2.41} z={0.1 + row * 0.58}
          w={0.75} h={0.04} d={0.52}
          topFill="#1a3a5c" leftFill="#1a3a5c" rightFill="#1a2a4c"
          stroke="#0369a1" strokeWidth={0.5} />
      )))}
      {(() => { const [sx, sy] = iso(3, 2.7, 1.2, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#fbbf24" fontSize="8" fontWeight="600">
            PV-01: 28 × 400 W panels on roof
          </text>
          <text x={sx} y={sy + 10} textAnchor="middle" fill="#64748b" fontSize="7">
            (+9 panels on ground mount)
          </text>
        </g>
      ); })()}

      {/* Battery bank (rear left) */}
      <IsoBox x={3.8} y={0} z={0.2} w={2.1} h={1.2} d={1.0}
        topFill="#0d2a1a" leftFill="#0a2015" rightFill="#0c2518"
        stroke="#065f46" strokeWidth={1} />
      {[0, 1, 2].map(c => [0, 1].map(r => (
        <IsoBox key={`bat-${c}-${r}`}
          x={3.9 + c * 0.65} y={0.05} z={0.3 + r * 0.42}
          w={0.55} h={1.05} d={0.35}
          topFill="#14532d" leftFill="#166534" rightFill="#15803d"
          stroke="#16a34a" strokeWidth={0.6} />
      )))}
      {(() => { const [sx, sy] = iso(4.85, 1.4, 0.7, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#86efac" fontSize="8" fontWeight="600">BAT-01</text>
          <text x={sx} y={sy + 10} textAnchor="middle" fill="#86efac" fontSize="8">LFP 87.5 kWh</text>
        </g>
      ); })()}

      {/* Inverter */}
      <IsoBox x={3.8} y={0} z={1.4} w={0.5} h={0.9} d={0.4}
        topFill="#1c1917" leftFill="#1c1917" rightFill="#292524"
        stroke="#44403c" strokeWidth={0.8} />
      {(() => { const [sx, sy] = iso(4.05, 1.1, 1.6, ox, oy, sc); return (
        <text x={sx} y={sy} textAnchor="middle" fill="#94a3b8" fontSize="7">INV-01</text>
      ); })()}

      {/* UF unit (F-01) */}
      <IsoBox x={0.2} y={0} z={0.4} w={0.3} h={1.4} d={0.3}
        topFill="#2e1065" leftFill="#2e1065" rightFill="#4c1d95"
        stroke="#7c3aed" strokeWidth={1} />
      {(() => { const [sx, sy] = iso(0.35, 1.6, 0.55, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#a78bfa" fontSize="8" fontWeight="600">F-01</text>
          <text x={sx} y={sy + 10} textAnchor="middle" fill="#a78bfa" fontSize="7">UF Pre-tx</text>
        </g>
      ); })()}

      {/* LP pump (P-01) */}
      <IsoBox x={0.7} y={0} z={0.4} w={0.3} h={0.4} d={0.3}
        topFill="#1e293b" leftFill="#1e293b" rightFill="#334155"
        stroke="#475569" strokeWidth={0.8} />
      {(() => { const [sx, sy] = iso(0.85, 0.55, 0.55, ox, oy, sc); return (
        <text x={sx} y={sy} textAnchor="middle" fill="#94a3b8" fontSize="7">P-01</text>
      ); })()}

      {/* HP pump (P-02) */}
      <IsoBox x={1.2} y={0} z={0.3} w={0.4} h={0.7} d={0.35}
        topFill="#1a0505" leftFill="#1a0505" rightFill="#2d1515"
        stroke="#ef4444" strokeWidth={1.2} />
      {(() => { const [sx, sy] = iso(1.4, 0.9, 0.48, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#f87171" fontSize="8" fontWeight="600">P-02</text>
          <text x={sx} y={sy + 10} textAnchor="middle" fill="#f87171" fontSize="7">HP 60 bar</text>
        </g>
      ); })()}

      {/* PX device (E-01) */}
      <IsoBox x={1.75} y={0} z={0.35} w={0.35} h={0.4} d={0.28}
        topFill="#0c2a3a" leftFill="#0c2a3a" rightFill="#103a4d"
        stroke="#0891b2" strokeWidth={1} strokeDasharray="3 2" />
      {(() => { const [sx, sy] = iso(1.92, 0.55, 0.49, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#67e8f9" fontSize="7" fontWeight="600">E-01</text>
          <text x={sx} y={sy + 9} textAnchor="middle" fill="#67e8f9" fontSize="6">PX 96%</text>
        </g>
      ); })()}

      {/* RO vessel (V-01) — long cylinder, horizontal */}
      {/* Simplified as elongated box */}
      <IsoBox x={2.2} y={0.1} z={0.35} w={3.0} h={0.35} d={0.25}
        topFill="#0c2233" leftFill="#0c2233" rightFill="#0e3045"
        stroke="#06b6d4" strokeWidth={1.5} />
      {/* End caps */}
      <IsoBox x={2.18} y={0.08} z={0.33} w={0.08} h={0.39} d={0.29}
        topFill="#0e7490" leftFill="#0e7490" rightFill="#0891b2"
        stroke="#06b6d4" strokeWidth={0.8} />
      <IsoBox x={5.2} y={0.08} z={0.33} w={0.08} h={0.39} d={0.29}
        topFill="#0e7490" leftFill="#0e7490" rightFill="#0891b2"
        stroke="#06b6d4" strokeWidth={0.8} />
      {/* Tie rods */}
      {[0.36, 0.55].map((z, i) => (
        <IsoBox key={i} x={2.2} y={0.15} z={z} w={3.0} h={0.02} d={0.01}
          topFill="#475569" leftFill="#475569" rightFill="#64748b"
          stroke="#64748b" strokeWidth={0.5} />
      ))}
      {/* Element divisions */}
      {[1, 2, 3, 4, 5].map(n => (
        <IsoBox key={n} x={2.2 + n * 0.5} y={0.09} z={0.34} w={0.02} h={0.37} d={0.27}
          topFill="#1e3a5f" leftFill="#1e3a5f" rightFill="#1e3a5f"
          stroke="#1e40af" strokeWidth={0.5} />
      ))}
      {(() => { const [sx, sy] = iso(3.7, 0.6, 0.47, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#67e8f9" fontSize="8" fontWeight="600">V-01 — RO Vessel</text>
          <text x={sx} y={sy + 11} textAnchor="middle" fill="#94a3b8" fontSize="7">
            6 × Filmtec SW30XHR-400i | 223 m²
          </text>
        </g>
      ); })()}

      {/* Permeate tank */}
      <IsoBox x={5.35} y={0} z={0.3} w={0.4} h={1.2} d={0.4}
        topFill="#0c2a1a" leftFill="#0c2a1a" rightFill="#14532d"
        stroke="#22c55e" strokeWidth={1} />
      {(() => { const [sx, sy] = iso(5.55, 1.4, 0.5, ox, oy, sc); return (
        <g>
          <text x={sx} y={sy} textAnchor="middle" fill="#86efac" fontSize="8" fontWeight="600">T-01</text>
          <text x={sx} y={sy + 10} textAnchor="middle" fill="#86efac" fontSize="7">Permeate</text>
          <text x={sx} y={sy + 20} textAnchor="middle" fill="#86efac" fontSize="7">20,000 L/d</text>
        </g>
      ); })()}

      {/* Process skid frame */}
      {[0.15, 0.95].map((z, i) => (
        <IsoBox key={i} x={0.15} y={-0.06} z={z} w={5.3} h={0.06} d={0.04}
          topFill="#1e293b" leftFill="#1e293b" rightFill="#334155"
          stroke="#475569" strokeWidth={0.6} />
      ))}

      {/* Flow paths */}
      {showFlow && (
        <g filter="url(#glow)">
          {/* Seawater in → LP pump */}
          <IsoArrow from={[-0.5, 0.2, 0.55]} to={[0.2, 0.2, 0.55]} color="#06b6d4" ox={ox} oy={oy} sc={sc} />
          {/* LP → UF */}
          <IsoArrow from={[0.5, 0.2, 0.55]} to={[0.72, 0.2, 0.55]} color="#06b6d4" ox={ox} oy={oy} sc={sc} />
          {/* UF → HP */}
          <IsoArrow from={[1.0, 0.2, 0.55]} to={[1.22, 0.2, 0.55]} color="#06b6d4" ox={ox} oy={oy} sc={sc} />
          {/* HP → RO */}
          <IsoArrow from={[1.62, 0.28, 0.48]} to={[2.2, 0.28, 0.48]} color="#06b6d4" ox={ox} oy={oy} sc={sc} />
          {/* RO → permeate */}
          <IsoArrow from={[5.28, 0.28, 0.5]} to={[5.35, 0.5, 0.5]} color="#22c55e" ox={ox} oy={oy} sc={sc} />
          {/* RO brine → PX */}
          <IsoArrow from={[5.28, 0.28, 0.38]} to={[5.28, 0.1, 0.38]} color="#f59e0b" ox={ox} oy={oy} sc={sc} />
          <IsoArrow from={[5.28, 0.1, 0.38]} to={[2.08, 0.1, 0.38]} color="#f59e0b" ox={ox} oy={oy} sc={sc} />
          {/* Brine out */}
          <IsoArrow from={[2.08, 0.1, 0.38]} to={[1.75, 0.1, 0.49]} color="#f59e0b" ox={ox} oy={oy} sc={sc} />
          {/* PX back to HP suction */}
          <IsoArrow from={[1.75, 0.2, 0.42]} to={[1.6, 0.2, 0.42]} color="#06b6d4" ox={ox} oy={oy} sc={sc} />
          {/* Electrical PV → battery */}
          <IsoArrow from={[3.0, 2.45, 1.0]} to={[4.5, 2.0, 0.8]} color="#fbbf24" ox={ox} oy={oy} sc={sc} />
          <IsoArrow from={[4.5, 2.0, 0.8]} to={[4.5, 1.2, 0.8]} color="#fbbf24" ox={ox} oy={oy} sc={sc} />
          <IsoArrow from={[4.5, 0.8, 0.8]} to={[1.4, 0.7, 0.5]} color="#fbbf24" ox={ox} oy={oy} sc={sc} />
        </g>
      )}

      {/* Dimension lines */}
      {showDimensions && (
        <g>
          {(() => {
            const [x1, y1] = iso(-0.2, 0, -0.3, ox, oy, sc);
            const [x2, y2] = iso(6.2, 0, -0.3, ox, oy, sc);
            return (
              <>
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#374151" strokeWidth="0.8" strokeDasharray="3 2" />
                <text x={(x1+x2)/2} y={(y1+y2)/2 - 8} textAnchor="middle" fill="#64748b" fontSize="7">L = 12.19 m (container)</text>
              </>
            );
          })()}
          {(() => {
            const [x1, y1] = iso(6.3, 0, -0.2, ox, oy, sc);
            const [x2, y2] = iso(6.3, 0, 2.6, ox, oy, sc);
            return (
              <>
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#374151" strokeWidth="0.8" strokeDasharray="3 2" />
                <text x={(x1+x2)/2 + 8} y={(y1+y2)/2} textAnchor="start" fill="#64748b" fontSize="7">W = 2.44 m</text>
              </>
            );
          })()}
          {(() => {
            const [x1, y1] = iso(-0.3, 0, 2.3, ox, oy, sc);
            const [x2, y2] = iso(-0.3, 2.4, 2.3, ox, oy, sc);
            return (
              <>
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#374151" strokeWidth="0.8" strokeDasharray="3 2" />
                <text x={x1 - 5} y={(y1+y2)/2} textAnchor="end" fill="#64748b" fontSize="7">H = 2.59 m</text>
              </>
            );
          })()}
          {/* RO vessel length */}
          {(() => {
            const [x1, y1] = iso(2.2, -0.1, 0.72, ox, oy, sc);
            const [x2, y2] = iso(5.2, -0.1, 0.72, ox, oy, sc);
            return (
              <>
                <line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#0891b2" strokeWidth="0.8" strokeDasharray="3 2" />
                <text x={(x1+x2)/2} y={(y1+y2)/2 + 12} textAnchor="middle" fill="#0891b2" fontSize="7">RO vessel L = 6.3 m (6 × 1016 mm + end caps)</text>
              </>
            );
          })()}
        </g>
      )}

      {/* Compass rose */}
      <g transform="translate(740, 420)">
        <line x1="0" y1="0" x2="15" y2="-8" stroke="#374151" strokeWidth="1.2" />
        <line x1="0" y1="0" x2="-15" y2="-8" stroke="#374151" strokeWidth="1.2" />
        <line x1="0" y1="0" x2="0" y2="-18" stroke="#374151" strokeWidth="1.2" />
        <text x="17" y="-5" fill="#475569" fontSize="7">X</text>
        <text x="-22" y="-5" fill="#475569" fontSize="7">Z</text>
        <text x="-4" y="-20" fill="#475569" fontSize="7">Y</text>
        <circle cx="0" cy="0" r="2" fill="#374151" />
      </g>

      {/* Title block */}
      <g transform="translate(30, 440)">
        <rect width="220" height="35" fill="#0f172a" stroke="#1e293b" />
        <text x="8" y="14" fill="#94a3b8" fontSize="8" fontWeight="600">ARCHMEDIS — SPRO SYSTEM</text>
        <text x="8" y="25" fill="#64748b" fontSize="7">Isometric view | Scale: NTS | 20,000 L/day</text>
        <text x="8" y="34" fill="#64748b" fontSize="6">All dims in metres unless noted</text>
      </g>
    </svg>
  );
}

// ─── TOP VIEW ──────────────────────────────────────────────────────────────
function TopView({ showDimensions, showFlow }: { showDimensions: boolean; showFlow: boolean }) {
  const W = 750; const H = 430;
  const scale = 80; // pixels per metre
  const ox = 50; const oy = 40; // origin

  // Container: 12.19 m × 2.44 m (40 ft ISO, schematic scale)
  const cW = scale * 6; const cH = 2.44 * scale; // 6 display units = 12.19 m

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full bg-slate-950">
      {/* Container */}
      <rect x={ox} y={oy} width={cW} height={cH} fill="#0a1628" stroke="#1e3a5f" strokeWidth="2" />
      <text x={ox + cW / 2} y={oy - 8} textAnchor="middle" fill="#1e3a5f" fontSize="9">
        40 ft ISO container — 12.19 × 2.44 m
      </text>

      {/* Solar panels (simplified grid) */}
      {[0,1,2,3].map(row => [0,1,2,3,4,5,6].map(col => (
        <rect key={`${row}-${col}`}
          x={ox + 5 + col * 65} y={oy + 5 + row * 46}
          width={58} height={40}
          fill="#1a3a5c" stroke="#0369a1" strokeWidth="0.5" />
      )))}
      <text x={ox + cW / 2} y={oy + 100} textAnchor="middle" fill="#fbbf24" fontSize="8" fontWeight="600">
        PV ARRAY — 28 panels on roof
      </text>

      {/* Process skid area — bottom half */}
      <rect x={ox + 10} y={oy + cH * 0.55} width={cW * 0.58} height={cH * 0.4}
        fill="#0a0a1a" stroke="#1e293b" strokeWidth="1" strokeDasharray="4 3" />
      <text x={ox + cW * 0.29 + 10} y={oy + cH * 0.55 - 5} fill="#334155" fontSize="7">PROCESS SKID</text>

      {/* Battery bank */}
      <rect x={ox + cW * 0.63} y={oy + cH * 0.15} width={cW * 0.33} height={cH * 0.65}
        fill="#0a2015" stroke="#065f46" strokeWidth="1.5" />
      {[0,1,2].map(c => [0,1].map(r => (
        <rect key={`bat${c}${r}`}
          x={ox + cW * 0.64 + c * (cW*0.105)} y={oy + cH*0.17 + r*(cH*0.3)}
          width={cW * 0.095} height={cH * 0.28}
          fill="#166534" stroke="#22c55e" strokeWidth="0.5" />
      )))}
      <text x={ox + cW * 0.795} y={oy + cH * 0.5} textAnchor="middle" fill="#86efac" fontSize="8">BAT-01</text>
      <text x={ox + cW * 0.795} y={oy + cH * 0.61} textAnchor="middle" fill="#86efac" fontSize="7">87.5 kWh</text>

      {/* Components on skid */}
      {/* UF */}
      <rect x={ox + 18} y={oy + cH * 0.58} width={22} height={70}
        fill="#2e1065" stroke="#7c3aed" strokeWidth="1" />
      <text x={ox + 29} y={oy + cH * 0.58 - 4} textAnchor="middle" fill="#a78bfa" fontSize="7">F-01</text>

      {/* LP pump */}
      <rect x={ox + 48} y={oy + cH * 0.61} width={22} height={22}
        fill="#1e293b" stroke="#475569" strokeWidth="1" />
      <text x={ox + 59} y={oy + cH * 0.61 - 4} textAnchor="middle" fill="#94a3b8" fontSize="7">P-01</text>

      {/* HP pump */}
      <rect x={ox + 78} y={oy + cH * 0.59} width={28} height={26}
        fill="#1a0505" stroke="#ef4444" strokeWidth="1.5" />
      <text x={ox + 92} y={oy + cH * 0.59 - 4} textAnchor="middle" fill="#f87171" fontSize="7">P-02</text>

      {/* PX */}
      <rect x={ox + 114} y={oy + cH * 0.6} width={24} height={22}
        fill="#0c2a3a" stroke="#0891b2" strokeWidth="1" strokeDasharray="3 2" />
      <text x={ox + 126} y={oy + cH * 0.6 - 4} textAnchor="middle" fill="#67e8f9" fontSize="7">E-01</text>

      {/* RO vessel — long horizontal */}
      <rect x={ox + 145} y={oy + cH * 0.6} width={cW * 0.47 - 5} height={18}
        fill="#0c2233" stroke="#06b6d4" strokeWidth="1.5" />
      {[1,2,3,4,5].map(n => (
        <line key={n} x1={ox + 145 + n * (cW*0.47-5)/6} y1={oy + cH*0.6}
          x2={ox + 145 + n * (cW*0.47-5)/6} y2={oy + cH*0.6 + 18}
          stroke="#1e40af" strokeWidth="0.5" />
      ))}
      <text x={ox + 145 + (cW*0.47-5)/2} y={oy + cH * 0.6 - 4} textAnchor="middle" fill="#67e8f9" fontSize="7">
        V-01 — RO vessel (6.3 m)
      </text>

      {/* Permeate tank */}
      <rect x={ox + cW * 0.58 - 30} y={oy + cH * 0.55} width={28} height={55}
        fill="#0c2a1a" stroke="#22c55e" strokeWidth="1.5" />
      <text x={ox + cW * 0.58 - 16} y={oy + cH * 0.55 - 4} textAnchor="middle" fill="#86efac" fontSize="7">T-01</text>

      {/* Flow paths */}
      {showFlow && (
        <g>
          {/* SW in */}
          <line x1={ox - 25} y1={oy + cH * 0.66} x2={ox + 18} y2={oy + cH * 0.66}
            stroke="#06b6d4" strokeWidth="2" markerEnd="url(#topArrowC)" />
          {/* UF → LP → HP → PX → RO */}
          <line x1={ox + 40} y1={oy + cH * 0.66} x2={ox + 48} y2={oy + cH * 0.66}
            stroke="#06b6d4" strokeWidth="2" markerEnd="url(#topArrowC)" />
          <line x1={ox + 70} y1={oy + cH * 0.66} x2={ox + 78} y2={oy + cH * 0.66}
            stroke="#06b6d4" strokeWidth="2" markerEnd="url(#topArrowC)" />
          <line x1={ox + 106} y1={oy + cH * 0.66} x2={ox + 114} y2={oy + cH * 0.66}
            stroke="#06b6d4" strokeWidth="2" markerEnd="url(#topArrowC)" />
          <line x1={ox + 138} y1={oy + cH * 0.66} x2={ox + 145} y2={oy + cH * 0.66}
            stroke="#06b6d4" strokeWidth="2.5" markerEnd="url(#topArrowC)" />
          {/* Permeate out */}
          <line x1={ox + 145 + (cW*0.47-5)} y1={oy + cH * 0.65} x2={ox + cW * 0.58 - 30} y2={oy + cH * 0.65}
            stroke="#22c55e" strokeWidth="2" markerEnd="url(#topArrowG)" />
          {/* Brine → PX */}
          <line x1={ox + 145 + (cW*0.47-5)} y1={oy + cH * 0.67} x2={ox + 145 + (cW*0.47-5) + 10} y2={oy + cH * 0.67}
            stroke="#f59e0b" strokeWidth="1.5" />
          <line x1={ox + 145 + (cW*0.47-5) + 10} y1={oy + cH * 0.67} x2={ox + 145 + (cW*0.47-5) + 10} y2={oy + cH * 0.79}
            stroke="#f59e0b" strokeWidth="1.5" />
          <line x1={ox + 145 + (cW*0.47-5) + 10} y1={oy + cH * 0.79} x2={ox + 126} y2={oy + cH * 0.79}
            stroke="#f59e0b" strokeWidth="1.5" markerEnd="url(#topArrowB)" />
          {/* PX → HP suction */}
          <line x1={ox + 114} y1={oy + cH * 0.72} x2={ox + 92} y2={oy + cH * 0.72}
            stroke="#06b6d4" strokeWidth="1.5" markerEnd="url(#topArrowC)" />
          {/* Electrical */}
          <line x1={ox + cW * 0.795} y1={oy + cH * 0.15} x2={ox + cW * 0.795} y2={oy + 10}
            stroke="#fbbf24" strokeWidth="1" strokeDasharray="4 3" />
          <line x1={ox + cW * 0.795} y1={oy + 10} x2={ox + 92} y2={oy + 10}
            stroke="#fbbf24" strokeWidth="1" strokeDasharray="4 3" />
          <line x1={ox + 92} y1={oy + 10} x2={ox + 92} y2={oy + cH * 0.59}
            stroke="#fbbf24" strokeWidth="1" strokeDasharray="4 3" markerEnd="url(#topArrowY)" />
        </g>
      )}

      {/* Dimension lines */}
      {showDimensions && (
        <g>
          <line x1={ox} y1={oy + cH + 20} x2={ox + cW} y2={oy + cH + 20}
            stroke="#374151" strokeWidth="0.8" />
          <line x1={ox} y1={oy + cH + 14} x2={ox} y2={oy + cH + 26} stroke="#374151" strokeWidth="0.8" />
          <line x1={ox + cW} y1={oy + cH + 14} x2={ox + cW} y2={oy + cH + 26} stroke="#374151" strokeWidth="0.8" />
          <text x={ox + cW / 2} y={oy + cH + 32} textAnchor="middle" fill="#64748b" fontSize="8">12.19 m</text>

          <line x1={ox + cW + 20} y1={oy} x2={ox + cW + 20} y2={oy + cH}
            stroke="#374151" strokeWidth="0.8" />
          <text x={ox + cW + 32} y={oy + cH / 2} textAnchor="start" fill="#64748b" fontSize="8" transform={`rotate(-90,${ox + cW + 32},${oy + cH / 2})`}>2.44 m</text>
        </g>
      )}

      {/* Markers */}
      <defs>
        <marker id="topArrowC" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 z" fill="#06b6d4" />
        </marker>
        <marker id="topArrowG" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 z" fill="#22c55e" />
        </marker>
        <marker id="topArrowB" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 z" fill="#f59e0b" />
        </marker>
        <marker id="topArrowY" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 z" fill="#fbbf24" />
        </marker>
      </defs>

      {/* Seawater label */}
      <text x={ox - 28} y={oy + cH * 0.63} fill="#06b6d4" fontSize="8">Seawater in →</text>

      {/* Title */}
      <text x={ox} y={H - 10} fill="#334155" fontSize="8">PLAN VIEW (from above) — Solar SPRO System | Scale: NTS</text>
    </svg>
  );
}

// ─── FRONT ELEVATION VIEW ──────────────────────────────────────────────────
function FrontView({ showDimensions }: { showDimensions: boolean }) {
  const ox = 60; const oy = 30;
  const sc = 80; // pixels/m
  const cW = 6.0 * sc; const cH = 2.59 * sc; // schematic scale; actual 12.19 m (40 ft)

  return (
    <svg viewBox="0 0 750 420" className="w-full bg-slate-950">
      {/* Container outline */}
      <rect x={ox} y={oy} width={cW} height={cH} fill="#0a1628" stroke="#1e3a5f" strokeWidth="2" />

      {/* Solar array on roof */}
      {[0,1,2,3,4,5,6].map(col => (
        <rect key={col} x={ox + 10 + col * 67} y={oy - 45} width={60} height={40}
          fill="#1a3a5c" stroke="#0369a1" strokeWidth="0.8" rx="2" />
      ))}
      <text x={ox + cW/2} y={oy - 50} textAnchor="middle" fill="#fbbf24" fontSize="8">
        PV ARRAY — 28 panels (400W each) — tilted south 15°
      </text>

      {/* Battery bank */}
      <rect x={ox + cW * 0.63} y={oy + 15} width={cW * 0.32} height={cH * 0.55}
        fill="#0a2015" stroke="#065f46" strokeWidth="1.5" />
      <text x={ox + cW * 0.79} y={oy + cH * 0.33} textAnchor="middle" fill="#86efac" fontSize="9" fontWeight="600">LFP</text>
      <text x={ox + cW * 0.79} y={oy + cH * 0.45} textAnchor="middle" fill="#86efac" fontSize="8">87.5 kWh</text>

      {/* Inverter above battery */}
      <rect x={ox + cW * 0.65} y={oy + cH * 0.6} width={cW * 0.12} height={cH * 0.28}
        fill="#1c1917" stroke="#44403c" strokeWidth="1" />
      <text x={ox + cW * 0.71} y={oy + cH * 0.76} textAnchor="middle" fill="#94a3b8" fontSize="7">INV-01</text>

      {/* RO vessel */}
      <rect x={ox + cW * 0.2} y={oy + cH * 0.25} width={cW * 0.41} height={35}
        fill="#0c2233" stroke="#06b6d4" strokeWidth="1.5" rx="17" />
      {[1,2,3,4,5].map(n => (
        <line key={n}
          x1={ox + cW * 0.2 + n * (cW*0.41)/6} y1={oy + cH * 0.25}
          x2={ox + cW * 0.2 + n * (cW*0.41)/6} y2={oy + cH * 0.25 + 35}
          stroke="#1e40af" strokeWidth="0.5" />
      ))}
      <text x={ox + cW * 0.41} y={oy + cH * 0.25 - 5} textAnchor="middle" fill="#67e8f9" fontSize="8">
        V-01 — RO vessel — 6 elements × SW30XHR-400i
      </text>

      {/* HP pump */}
      <rect x={ox + cW * 0.12} y={oy + cH * 0.28} width={40} height={55}
        fill="#1a0505" stroke="#ef4444" strokeWidth="1.5" rx="4" />
      <text x={ox + cW * 0.12 + 20} y={oy + cH * 0.28 - 5} textAnchor="middle" fill="#f87171" fontSize="8">P-02</text>
      <text x={ox + cW * 0.12 + 20} y={oy + cH * 0.28 + 30} textAnchor="middle" fill="#f87171" fontSize="7">60 bar</text>

      {/* UF */}
      <rect x={ox + 20} y={oy + cH * 0.2} width={28} height={130}
        fill="#2e1065" stroke="#7c3aed" strokeWidth="1.2" rx="14" />
      <text x={ox + 34} y={oy + cH * 0.2 - 6} textAnchor="middle" fill="#a78bfa" fontSize="8">F-01</text>

      {/* PX */}
      <rect x={ox + cW * 0.14} y={oy + cH * 0.52} width={32} height={28}
        fill="#0c2a3a" stroke="#0891b2" strokeWidth="1" strokeDasharray="3 2" />
      <text x={ox + cW * 0.14 + 16} y={oy + cH * 0.52 - 5} textAnchor="middle" fill="#67e8f9" fontSize="7">E-01 PX</text>

      {/* Ground line */}
      <line x1={ox - 20} y1={oy + cH} x2={ox + cW + 20} y2={oy + cH} stroke="#374151" strokeWidth="1.5" />
      {Array.from({length: 25}, (_, i) => (
        <line key={i} x1={ox - 20 + i * 32} y1={oy + cH} x2={ox - 20 + i * 32 - 8} y2={oy + cH + 8}
          stroke="#374151" strokeWidth="1" />
      ))}

      {/* Dimension lines */}
      {showDimensions && (
        <g>
          {/* Width */}
          <line x1={ox} y1={oy + cH + 25} x2={ox + cW} y2={oy + cH + 25} stroke="#374151" strokeWidth="0.8" />
          <line x1={ox} y1={oy + cH + 18} x2={ox} y2={oy + cH + 32} stroke="#374151" strokeWidth="0.8" />
          <line x1={ox + cW} y1={oy + cH + 18} x2={ox + cW} y2={oy + cH + 32} stroke="#374151" strokeWidth="0.8" />
          <text x={ox + cW/2} y={oy + cH + 37} textAnchor="middle" fill="#64748b" fontSize="8">12.19 m</text>

          {/* Height */}
          <line x1={ox - 25} y1={oy} x2={ox - 25} y2={oy + cH} stroke="#374151" strokeWidth="0.8" />
          <text x={ox - 30} y={oy + cH/2} textAnchor="middle" fill="#64748b" fontSize="8"
            transform={`rotate(-90,${ox-30},${oy+cH/2})`}>2.59 m</text>

          {/* RO vessel inner dim */}
          <line x1={ox + cW * 0.2} y1={oy + cH * 0.25 + 50} x2={ox + cW * 0.61} y2={oy + cH * 0.25 + 50}
            stroke="#0891b2" strokeWidth="0.8" strokeDasharray="3 2" />
          <text x={ox + cW * 0.41} y={oy + cH * 0.25 + 62} textAnchor="middle" fill="#0891b2" fontSize="7">
            RO vessel: 6.3 m × OD 225 mm
          </text>

          {/* UF height */}
          <line x1={ox + 56} y1={oy + cH * 0.2} x2={ox + 56} y2={oy + cH * 0.2 + 130}
            stroke="#7c3aed" strokeWidth="0.8" strokeDasharray="3 2" />
          <text x={ox + 65} y={oy + cH * 0.2 + 65} fill="#7c3aed" fontSize="7">UF: L=1.2m</text>
        </g>
      )}

      {/* Title */}
      <text x={ox} y={390} fill="#334155" fontSize="8">FRONT ELEVATION — Solar SPRO System | Scale: NTS</text>
    </svg>
  );
}

// ─── P&ID VIEW ──────────────────────────────────────────────────────────────
function PIDView({ showFlow }: { showFlow: boolean }) {
  return (
    <svg viewBox="0 0 800 440" className="w-full bg-slate-950">
      <defs>
        {["C", "G", "B", "Y", "V"].map(c => (
          <marker key={c} id={`pid${c}`} markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
            <path d="M0,0 L7,3.5 L0,7 z"
              fill={c === "C" ? "#06b6d4" : c === "G" ? "#22c55e" : c === "B" ? "#f59e0b" : c === "V" ? "#a78bfa" : "#fbbf24"} />
          </marker>
        ))}
      </defs>

      {/* Title */}
      <rect x={10} y={8} width={780} height={22} fill="#0f172a" stroke="#1e293b" />
      <text x={400} y={23} textAnchor="middle" fill="#94a3b8" fontSize="10" fontWeight="600">
        PROCESS & INSTRUMENTATION DIAGRAM — SOLAR SPRO SYSTEM | ARCHMEDIS | SHEET 1 OF 1
      </text>

      {/* === Seawater source === */}
      <rect x={10} y={120} width={55} height={45} rx="4" fill="#1e293b" stroke="#374151" />
      <text x={37} y={138} textAnchor="middle" fill="#94a3b8" fontSize="8" fontWeight="600">SEAWATER</text>
      <text x={37} y={149} textAnchor="middle" fill="#06b6d4" fontSize="8">44.4 m³/d</text>
      <text x={37} y={158} textAnchor="middle" fill="#64748b" fontSize="7">35 g/L NaCl</text>

      {/* === Antiscalant dosing === */}
      <rect x={75} y={80} width={50} height={35} rx="3" fill="#1e293b" stroke="#a78bfa" strokeDasharray="3 2" />
      <text x={100} y={94} textAnchor="middle" fill="#a78bfa" fontSize="8" fontWeight="600">ANTI-</text>
      <text x={100} y={105} textAnchor="middle" fill="#a78bfa" fontSize="8">SCALANT</text>
      <text x={100} y={113} textAnchor="middle" fill="#64748b" fontSize="6">D-01</text>

      {/* === LP pump === */}
      <circle cx={150} cy={142} r={18} fill="#1e293b" stroke="#374151" />
      <path d="M138,142 Q150,130 162,142 Q150,154 138,142" fill="#374151" />
      <text x={150} y={138} textAnchor="middle" fill="#94a3b8" fontSize="7" fontWeight="600">P</text>
      <text x={150} y={148} textAnchor="middle" fill="#94a3b8" fontSize="7">P-01</text>
      <text x={150} y={168} textAnchor="middle" fill="#64748b" fontSize="6">2.5 bar</text>

      {/* FI-01 instrument */}
      <circle cx={150} cy={185} r={10} fill="#0f172a" stroke="#374151" />
      <text x={150} y={189} textAnchor="middle" fill="#64748b" fontSize="6">FI-01</text>
      <line x1={150} y1={160} x2={150} y2={175} stroke="#374151" strokeWidth="0.8" strokeDasharray="2 2" />

      {/* === UF pre-treatment === */}
      <rect x={185} y={108} width={60} height={65} rx="6" fill="#1e293b" stroke="#7c3aed" />
      <text x={215} y={128} textAnchor="middle" fill="#a78bfa" fontSize="8" fontWeight="600">UF PRE-TX</text>
      <text x={215} y={140} textAnchor="middle" fill="#94a3b8" fontSize="7">SDI &lt; 3</text>
      <text x={215} y={152} textAnchor="middle" fill="#94a3b8" fontSize="7">0.02 μm</text>
      <text x={215} y={164} textAnchor="middle" fill="#64748b" fontSize="6">F-01</text>

      {/* Instruments on UF */}
      {[["PT-01", 192, 97], ["AT-01", 225, 97]].map(([lbl, x, y]) => (
        <g key={lbl as string}>
          <rect x={x as number - 12} y={y as number - 9} width={24} height={14} rx="2" fill="#0f172a" stroke="#374151" />
          <text x={x as number} y={y as number} textAnchor="middle" fill="#64748b" fontSize="6">{lbl}</text>
          <line x1={x as number} y1={y as number + 5} x2={x as number} y2="108" stroke="#374151" strokeWidth="0.5" strokeDasharray="2 2" />
        </g>
      ))}

      {/* === HP pump === */}
      <circle cx={300} cy={142} r={22} fill="#1a0505" stroke="#ef4444" strokeWidth="1.5" />
      <path d="M285,142 Q300,125 315,142 Q300,159 285,142" fill="#2d0a0a" />
      <text x={300} y={138} textAnchor="middle" fill="#f87171" fontSize="8" fontWeight="600">P</text>
      <text x={300} y={149} textAnchor="middle" fill="#f87171" fontSize="8">P-02</text>
      <text x={300} y={172} textAnchor="middle" fill="#f87171" fontSize="7">60 bar</text>

      {/* PT-02 */}
      <circle cx={300} cy={108} r={10} fill="#0f172a" stroke="#374151" />
      <text x={300} y={112} textAnchor="middle" fill="#64748b" fontSize="6">PT-02</text>
      <line x1={300} y1={118} x2={300} y2={120} stroke="#374151" strokeWidth="0.8" strokeDasharray="2 2" />

      {/* === PX device === */}
      <rect x={345} y={165} width={55} height={40} rx="4" fill="#0c2a3a" stroke="#0891b2" strokeDasharray="4 2" />
      <text x={372} y={181} textAnchor="middle" fill="#67e8f9" fontSize="8" fontWeight="600">PX DEVICE</text>
      <text x={372} y={193} textAnchor="middle" fill="#94a3b8" fontSize="7">η = 96%</text>
      <text x={372} y={201} textAnchor="middle" fill="#64748b" fontSize="6">E-01</text>

      {/* === RO Vessel === */}
      <rect x={415} y={95} width={230} height={95} rx="8" fill="#0c2233" stroke="#06b6d4" strokeWidth="1.5" />
      {[1,2,3,4,5].map(n => (
        <line key={n} x1={415 + n * 38} y1={95} x2={415 + n * 38} y2={190}
          stroke="#1e40af" strokeWidth="0.5" />
      ))}
      <text x={530} y={118} textAnchor="middle" fill="#67e8f9" fontSize="9" fontWeight="600">RO PRESSURE VESSEL — V-01</text>
      <text x={530} y={132} textAnchor="middle" fill="#94a3b8" fontSize="8">6 × Filmtec SW30XHR-400i | 223 m² active area</text>
      <text x={530} y={146} textAnchor="middle" fill="#94a3b8" fontSize="8">Feed: 44.4 m³/d at 60 bar | Recovery: 45%</text>
      <text x={530} y={160} textAnchor="middle" fill="#22c55e" fontSize="8">Permeate: 20,000 L/d | Rejection: 99.75%</text>
      <text x={530} y={174} textAnchor="middle" fill="#f59e0b" fontSize="7">Brine: 24,400 L/d at 63.6 g/L NaCl</text>

      {/* Instruments on RO */}
      {[["PI-01", 430, 84], ["PT-03", 475, 84], ["AT-02", 520, 84], ["FI-02", 565, 84], ["PI-02", 610, 84]].map(([lbl, x, y]) => (
        <g key={lbl as string}>
          <rect x={x as number - 14} y={y as number - 9} width={28} height={14} rx="2" fill="#0f172a" stroke="#374151" />
          <text x={x as number} y={y as number} textAnchor="middle" fill="#64748b" fontSize="6">{lbl}</text>
          <line x1={x as number} y1={y as number + 5} x2={x as number} y2="95" stroke="#374151" strokeWidth="0.5" strokeDasharray="2 2" />
        </g>
      ))}

      {/* === Permeate storage === */}
      <rect x={660} y={95} width={70} height={70} rx="6" fill="#0c2a1a" stroke="#22c55e" />
      <text x={695} y={125} textAnchor="middle" fill="#86efac" fontSize="8" fontWeight="600">PERMEATE</text>
      <text x={695} y={138} textAnchor="middle" fill="#86efac" fontSize="8">STORAGE</text>
      <text x={695} y={152} textAnchor="middle" fill="#86efac" fontSize="8">T-01</text>
      <text x={695} y={165} textAnchor="middle" fill="#94a3b8" fontSize="7">20,000 L/d</text>

      {/* LI on tank */}
      <circle cx={695} cy={83} r={10} fill="#0f172a" stroke="#374151" />
      <text x={695} y={87} textAnchor="middle" fill="#64748b" fontSize="6">LI-01</text>
      <line x1={695} y1={93} x2={695} y2={95} stroke="#374151" strokeWidth="0.8" />

      {/* === Brine disposal === */}
      <rect x={660} y={230} width={70} height={40} rx="4" fill="#1a1000" stroke="#f59e0b" />
      <text x={695} y={248} textAnchor="middle" fill="#fcd34d" fontSize="8" fontWeight="600">BRINE</text>
      <text x={695} y={260} textAnchor="middle" fill="#94a3b8" fontSize="8">DISPOSAL</text>
      <text x={695} y={268} textAnchor="middle" fill="#64748b" fontSize="6">diffuser</text>

      {/* === PV + Battery (top section) === */}
      <rect x={20} y={290} width={90} height={55} rx="4" fill="#1e293b" stroke="#fbbf24" />
      <text x={65} y={308} textAnchor="middle" fill="#fbbf24" fontSize="8" fontWeight="600">PV ARRAY</text>
      <text x={65} y={320} textAnchor="middle" fill="#94a3b8" fontSize="7">14.8 kW_peak</text>
      <text x={65} y={332} textAnchor="middle" fill="#94a3b8" fontSize="7">MPPT: INV-01</text>

      <rect x={125} y={290} width={80} height={55} rx="4" fill="#0a2015" stroke="#22c55e" />
      <text x={165} y={308} textAnchor="middle" fill="#86efac" fontSize="8" fontWeight="600">LFP BATTERY</text>
      <text x={165} y={320} textAnchor="middle" fill="#86efac" fontSize="7">87.5 kWh</text>
      <text x={165} y={332} textAnchor="middle" fill="#94a3b8" fontSize="7">48V system</text>

      {/* Flow lines */}
      {showFlow && (
        <g>
          {/* SW → LP pump */}
          <line x1={65} y1={142} x2={132} y2={142} stroke="#06b6d4" strokeWidth="2" markerEnd="url(#pidC)" />
          {/* Antiscalant dosing */}
          <line x1={100} y1={115} x2={120} y2={130} stroke="#a78bfa" strokeWidth="1" strokeDasharray="3 2" markerEnd="url(#pidV)" />
          {/* LP → UF */}
          <line x1={168} y1={142} x2={185} y2={142} stroke="#06b6d4" strokeWidth="2" markerEnd="url(#pidC)" />
          {/* UF → HP */}
          <line x1={245} y1={142} x2={278} y2={142} stroke="#06b6d4" strokeWidth="2" markerEnd="url(#pidC)" />
          {/* HP → RO */}
          <line x1={322} y1={142} x2={415} y2={142} stroke="#06b6d4" strokeWidth="2.5" markerEnd="url(#pidC)" />
          {/* Pressure label */}
          <rect x={350} y={126} width={42} height={14} rx="3" fill="#7f1d1d" stroke="#ef4444" />
          <text x={371} y={136} textAnchor="middle" fill="#fca5a5" fontSize="7">60 bar →</text>
          {/* RO → permeate */}
          <line x1={645} y1={130} x2={660} y2={130} stroke="#22c55e" strokeWidth="2" markerEnd="url(#pidG)" />
          {/* RO → brine PX */}
          <line x1={645} y1={162} x2={680} y2={162} stroke="#f59e0b" strokeWidth="1.8" />
          <line x1={680} y1={162} x2={680} y2={215} stroke="#f59e0b" strokeWidth="1.8" />
          <line x1={680} y1={215} x2={695} y2={230} stroke="#f59e0b" strokeWidth="1.8" markerEnd="url(#pidB)" />
          {/* Also brine → PX */}
          <line x1={645} y1={170} x2={680} y2={170} stroke="#f59e0b" strokeWidth="1.2" />
          <line x1={680} y1={170} x2={680} y2={195} stroke="#f59e0b" strokeWidth="1.2" />
          <line x1={680} y1={195} x2={400} y2={195} stroke="#f59e0b" strokeWidth="1.2" markerEnd="url(#pidB)" />
          {/* PX → HP suction (energy recovery) */}
          <line x1={345} y1={185} x2={325} y2={185} stroke="#06b6d4" strokeWidth="1.5" />
          <line x1={325} y1={185} x2={325} y2={162} stroke="#06b6d4" strokeWidth="1.5" markerEnd="url(#pidC)" />
          {/* PX energy recovery arrow label */}
          <text x={360} y={215} fill="#67e8f9" fontSize="7">← pressure recovery 96% →</text>
          {/* Electrical PV → battery → P-02 */}
          <line x1={110} y1={317} x2={125} y2={317} stroke="#fbbf24" strokeWidth="1.2" markerEnd="url(#pidY)" />
          <line x1={205} y1={317} x2={300} y2={317} stroke="#fbbf24" strokeWidth="1.2" />
          <line x1={300} y1={317} x2={300} y2={165} stroke="#fbbf24" strokeWidth="1.2" markerEnd="url(#pidY)" />
          <text x={220} y={310} fill="#fbbf24" fontSize="7">DC power: 70 kWh/day to HP pump</text>
        </g>
      )}

      {/* Legend */}
      <g transform="translate(20, 375)">
        {[
          ["#06b6d4", "Feed (seawater / recovered)"],
          ["#22c55e", "Permeate (freshwater)"],
          ["#f59e0b", "Brine reject"],
          ["#fbbf24", "DC electrical"],
          ["#a78bfa", "Chemical dosing"],
        ].map(([col, lbl], i) => (
          <g key={i} transform={`translate(${i * 148}, 0)`}>
            <line x1={0} y1={7} x2={20} y2={7} stroke={col} strokeWidth="2" />
            <text x={25} y={11} fill="#64748b" fontSize="7">{lbl}</text>
          </g>
        ))}
      </g>

      <text x={10} y={420} fill="#334151" fontSize="7">
        P&ID — ARCHMEDIS SOLAR SPRO | 20,000 L/day | Rev A | Instruments: FI=Flow, PT=Pressure, AT=Analytical, LI=Level
      </text>
    </svg>
  );
}
