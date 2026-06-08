"""Generate all 5 CAD engineering SVG drawings for deliverables/02_cad_concept/
Canvas: 1200 × 780 px — wide enough to fit all labels without clipping.
"""
import os, math

os.makedirs("deliverables/02_cad_concept", exist_ok=True)

# ── shared marker defs ──────────────────────────────────────────────────────
DEFS = """<defs>
  <marker id="aC" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M0,1 L7,4 L0,7 z" fill="#1565c0"/></marker>
  <marker id="aG" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M0,1 L7,4 L0,7 z" fill="#2e7d32"/></marker>
  <marker id="aO" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M0,1 L7,4 L0,7 z" fill="#bf5600"/></marker>
  <marker id="aY" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M0,1 L7,4 L0,7 z" fill="#e67e22"/></marker>
  <marker id="dL" markerWidth="8" markerHeight="8" refX="0" refY="4" orient="auto">
    <path d="M7,0.5 L0,4 L7,7.5" fill="none" stroke="#555" stroke-width="1.2"/></marker>
  <marker id="dR" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto">
    <path d="M0,0.5 L8,4 L0,7.5" fill="none" stroke="#555" stroke-width="1.2"/></marker>
</defs>"""

W, H = 1200, 780   # canvas dimensions for all drawings


def svg_wrap(content, w=W, h=H):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        + f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        + f'<rect width="{w}" height="{h}" fill="#f0f2f5"/>'
        + f'<rect x="8" y="8" width="{w-16}" height="{h-56}" fill="white" stroke="#333" stroke-width="1.5"/>'
        + DEFS
        + content
        + "</svg>"
    )


def title_block(dwgno, title, subtitle, scale, w=W, h=H):
    tb_y = h - 44
    return (
        f'<rect x="8" y="{tb_y}" width="{w-16}" height="36" fill="#2c3e50"/>'
        f'<rect x="8" y="{tb_y}" width="290" height="36" fill="#1a2b3c"/>'
        f'<text x="154" y="{tb_y+14}" text-anchor="middle" font-family="Arial" font-size="9" font-weight="bold" fill="#f0f0f0">ARCHMEDIS TECHNICAL TRIAL — ROUND 2</text>'
        f'<text x="154" y="{tb_y+28}" text-anchor="middle" font-family="Arial" font-size="8" fill="#bdc3c7">Candidate Submission | June 2026</text>'
        f'<text x="{w//2}" y="{tb_y+14}" text-anchor="middle" font-family="Arial" font-size="12" font-weight="bold" fill="white">{title}</text>'
        f'<text x="{w//2}" y="{tb_y+29}" text-anchor="middle" font-family="Arial" font-size="9" fill="#bdc3c7">{subtitle}</text>'
        f'<text x="{w-14}" y="{tb_y+11}" text-anchor="end" font-family="Arial" font-size="7.5" fill="#bdc3c7">DWG: {dwgno} | Rev A</text>'
        f'<text x="{w-14}" y="{tb_y+22}" text-anchor="end" font-family="Arial" font-size="7.5" fill="#bdc3c7">Scale: {scale}</text>'
        f'<text x="{w-14}" y="{tb_y+33}" text-anchor="end" font-family="Arial" font-size="7.5" fill="#bdc3c7">20,000 L/day SWRO</text>'
    )


def hdim(x1, y1, x2, text, col="#555", fs=7.5):
    xm = (x1 + x2) / 2
    yt = y1 - 5
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x1:.1f}" y2="{yt:.1f}" stroke="{col}" stroke-width="0.8"/>'
        f'<line x1="{x2:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{yt:.1f}" stroke="{col}" stroke-width="0.8"/>'
        f'<line x1="{x1:.1f}" y1="{yt:.1f}" x2="{x2:.1f}" y2="{yt:.1f}" stroke="{col}" stroke-width="0.8" marker-start="url(#dL)" marker-end="url(#dR)"/>'
        f'<text x="{xm:.1f}" y="{yt-3:.1f}" text-anchor="middle" font-size="{fs}" font-family="Arial" fill="{col}">{text}</text>'
    )


def vdim(x, y1, y2, text, col="#555", fs=7.5):
    ym = (y1 + y2) / 2
    xt = x - 5
    return (
        f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{xt:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="0.8"/>'
        f'<line x1="{x:.1f}" y1="{y2:.1f}" x2="{xt:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.8"/>'
        f'<line x1="{xt:.1f}" y1="{y1:.1f}" x2="{xt:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="0.8" marker-start="url(#dL)" marker-end="url(#dR)"/>'
        f'<text x="{xt-4:.1f}" y="{ym:.1f}" text-anchor="middle" font-size="{fs}" font-family="Arial" fill="{col}" transform="rotate(-90 {xt-4:.1f} {ym:.1f})">{text}</text>'
    )


def inst(cx, cy, tag, lcx=None, lcy=None):
    """ISA instrument bubble (circle + tag text, optional leader line)."""
    s = (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="10" fill="white" stroke="#333" stroke-width="1.2"/>'
        f'<text x="{cx:.1f}" y="{cy+3.8:.1f}" text-anchor="middle" font-family="Arial" font-size="7" fill="#111">{tag}</text>'
    )
    if lcx is not None:
        s += (
            f'<line x1="{cx:.1f}" y1="{cy+10:.1f}" x2="{lcx:.1f}" y2="{lcy:.1f}"'
            f' stroke="#555" stroke-width="0.9" stroke-dasharray="3,2"/>'
        )
    return s


def txt(x, y, s, anchor="middle", fs=8, fill="#111", bold=False, col=None):
    fw = ' font-weight="bold"' if bold else ""
    fc = col or fill
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-family="Arial" font-size="{fs}" fill="{fc}"{fw}>{s}</text>'


# ════════════════════════════════════════════════════════════════════════════
# 1. PLAN VIEW  (top-down, 1:60)
# Container: 12.19 m × 2.44 m
# ════════════════════════════════════════════════════════════════════════════
PPM = 62.0          # px per metre
CX0, CY0 = 96, 130  # container origin (top-left)
CW = 12.19 * PPM    # ≈ 756 px
CH = 2.44 * PPM     # ≈ 151 px


def px(m): return CX0 + m * PPM
def py(m): return CY0 + m * PPM


plan = []
plan.append(txt(W/2, 26, "PLAN VIEW (TOP) — SOLAR-POWERED SWRO DESALINATION — 20,000 L/DAY", fs=13, bold=True, fill="#1a3a6b"))
plan.append(txt(W/2, 42, "Scale 1:60  |  40 ft ISO Container (12.19 × 2.44 m)  |  All dimensions in metres", fs=9, fill="#555"))

# Zone shading
plan.append(f'<rect x="{px(0):.1f}" y="{py(0):.1f}" width="{2.0*PPM:.1f}" height="{CH:.1f}" fill="#e8eaf6" opacity="0.55"/>')
plan.append(f'<rect x="{px(2.0):.1f}" y="{py(0):.1f}" width="{2.5*PPM:.1f}" height="{CH:.1f}" fill="#fce4ec" opacity="0.55"/>')
plan.append(f'<rect x="{px(4.5):.1f}" y="{py(0):.1f}" width="{6.5*PPM:.1f}" height="{CH:.1f}" fill="#e3f2fd" opacity="0.55"/>')
plan.append(f'<rect x="{px(11.0):.1f}" y="{py(0):.1f}" width="{1.19*PPM:.1f}" height="{CH:.1f}" fill="#e8f5e9" opacity="0.55"/>')

# Container outline
plan.append(f'<rect x="{CX0:.1f}" y="{CY0:.1f}" width="{CW:.1f}" height="{CH:.1f}" fill="none" stroke="#1a3a6b" stroke-width="2.5"/>')

# Zone dividers
for v in [2.0, 4.5, 11.0]:
    plan.append(f'<line x1="{px(v):.1f}" y1="{CY0:.1f}" x2="{px(v):.1f}" y2="{CY0+CH:.1f}" stroke="#999" stroke-width="1" stroke-dasharray="6,3"/>')

# Element dividers inside RO vessel zone
for i in range(1, 6):
    xd = px(4.5 + i * 6.5 / 6)
    plan.append(f'<line x1="{xd:.1f}" y1="{py(1.08):.1f}" x2="{xd:.1f}" y2="{py(1.36):.1f}" stroke="#1565c0" stroke-width="0.9" opacity="0.55"/>')

# Zone labels (below container)
lbl_y = CY0 + CH + 16
plan.append(txt(px(1.0),   lbl_y, "ZONE A: Pre-Treatment", fs=8, fill="#4527a0"))
plan.append(txt(px(3.25),  lbl_y, "ZONE B: HP + PX", fs=8, fill="#c62828"))
plan.append(txt(px(7.75),  lbl_y, "ZONE C: RO Vessel (6.5 m)", fs=8, fill="#1565c0"))
plan.append(txt(px(11.6),  lbl_y, "ZONE D", fs=8, fill="#2e7d32"))

# ── Battery bank ────────────────────────────────────────────────────────────
bx0, bw = px(0.1), 3.8 * PPM
bh = 0.52 * PPM
by0 = py(0.06)
plan.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.4" rx="3"/>')
plan.append(txt(bx0 + bw/2, by0 + 14, "LFP BATTERY BANK — BAT-01", fs=9, bold=True, fill="#1b5e20"))
plan.append(txt(bx0 + bw/2, by0 + 25, "87.5 kWh | 48 V | 4 racks × 1.0 m  |  CATL 280 Ah prismatic | 80% DoD", fs=7.5, fill="#2e7d32"))
plan.append(txt(bx0 + bw/2, by0 + 36, "1-day autonomy | BMS: Daly 48V 200A", fs=7, fill="#388e3c"))

# ── Inverter ────────────────────────────────────────────────────────────────
ivx0, ivw = px(2.2), 0.68 * PPM
ivh = 0.56 * PPM
ivy0 = py(0.67)
plan.append(f'<rect x="{ivx0:.1f}" y="{ivy0:.1f}" width="{ivw:.1f}" height="{ivh:.1f}" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="1.2" rx="3"/>')
plan.append(txt(ivx0 + ivw/2, ivy0 + 13, "INV-01", fs=8.5, bold=True, fill="#4a148c"))
plan.append(txt(ivx0 + ivw/2, ivy0 + 25, "Victron 48/8000", fs=7.5, fill="#6a1b9a"))
plan.append(txt(ivx0 + ivw/2, ivy0 + 36, "8 kW | MPPT", fs=7, fill="#6a1b9a"))

# ── Antiscalant dosing D-01 ─────────────────────────────────────────────────
dsx, dsw = px(0.1), 0.5 * PPM
dsh = 0.45 * PPM
dsy = py(0.67)
plan.append(f'<rect x="{dsx:.1f}" y="{dsy:.1f}" width="{dsw:.1f}" height="{dsh:.1f}" fill="#fce4ec" stroke="#ad1457" stroke-width="1" stroke-dasharray="5,2" rx="3"/>')
plan.append(txt(dsx + dsw/2, dsy + 14, "D-01", fs=8.5, bold=True, fill="#880e4f"))
plan.append(txt(dsx + dsw/2, dsy + 26, "Antiscalant", fs=7.5, fill="#ad1457"))
plan.append(txt(dsx + dsw/2, dsy + 37, "&lt;5 ppm", fs=7, fill="#ad1457"))

# ── UF skid F-01 ────────────────────────────────────────────────────────────
ufx0, ufw = px(0.68), 1.0 * PPM
ufh = 1.3 * PPM
ufy0 = py(0.82)
plan.append(f'<rect x="{ufx0:.1f}" y="{ufy0:.1f}" width="{ufw:.1f}" height="{ufh:.1f}" fill="#ede7f6" stroke="#5c35cc" stroke-width="1.6" rx="4"/>')
plan.append(txt(ufx0 + ufw/2, ufy0 + ufw*0.45, "UF PRE-TX", fs=9, bold=True, fill="#4527a0"))
plan.append(txt(ufx0 + ufw/2, ufy0 + ufw*0.6,  "F-01", fs=8.5, fill="#512da8"))
plan.append(txt(ufx0 + ufw/2, ufy0 + ufw*0.75, "Dow FilmTec 0.02 µm", fs=7, fill="#5c35cc"))
plan.append(txt(ufx0 + ufw/2, ufy0 + ufw*0.9,  "SDI &lt;3 | PVDF", fs=7, fill="#5c35cc"))

# Instrument bubbles above UF
plan.append(inst(px(0.82), py(0.70), "PT-01", px(0.82), ufy0))
plan.append(inst(px(1.38), py(0.70), "AT-01", px(1.38), ufy0))

# ── LP Pump P-01 ─────────────────────────────────────────────────────────────
p01x, p01y = px(0.38), py(1.52)
plan.append(f'<circle cx="{p01x:.1f}" cy="{p01y:.1f}" r="22" fill="#fff8e1" stroke="#f57f17" stroke-width="1.8"/>')
plan.append(txt(p01x, p01y - 5, "P-01", fs=8.5, bold=True, fill="#e65100"))
plan.append(txt(p01x, p01y + 7, "LP 2.5 bar", fs=7.5, fill="#e65100"))
# dosing line D-01 → feed pipe
plan.append(f'<line x1="{px(0.35):.1f}" y1="{dsy+dsh:.1f}" x2="{px(0.35):.1f}" y2="{p01y-22:.1f}" stroke="#ad1457" stroke-width="1.2" stroke-dasharray="4,2" marker-end="url(#aY)"/>')

# ── HP Pump P-02 ─────────────────────────────────────────────────────────────
p02x, p02y = px(2.72), py(1.5)
plan.append(f'<circle cx="{p02x:.1f}" cy="{p02y:.1f}" r="26" fill="#ffebee" stroke="#c62828" stroke-width="2.2"/>')
plan.append(txt(p02x, p02y - 8, "P-02", fs=9, bold=True, fill="#b71c1c"))
plan.append(txt(p02x, p02y + 5, "HP 60 bar", fs=8, fill="#c62828"))
plan.append(txt(p02x, p02y + 16, "5.5 kW | MTRE", fs=7, fill="#c62828"))

# PSV
psvy0 = py(0.66)
psvh = 0.24 * PPM
plan.append(f'<rect x="{px(2.48):.1f}" y="{psvy0:.1f}" width="{0.48*PPM:.1f}" height="{psvh:.1f}" fill="#fff3e0" stroke="#e65100" stroke-width="0.9" rx="2"/>')
plan.append(txt(p02x, psvy0 + psvh*0.4, "PSV-01", fs=7.5, bold=True, fill="#e65100"))
plan.append(txt(p02x, psvy0 + psvh*0.8, "set 70 bar", fs=7, fill="#e65100"))
plan.append(f'<line x1="{p02x:.1f}" y1="{psvy0+psvh:.1f}" x2="{p02x:.1f}" y2="{p02y-26:.1f}" stroke="#e65100" stroke-width="0.8" stroke-dasharray="3,2"/>')
plan.append(inst(p02x, py(0.50), "PT-02", p02x, psvy0))

# ── PX device E-01 ───────────────────────────────────────────────────────────
pxx0, pxw = px(3.25), 0.9 * PPM
pxh = 0.9 * PPM
pxy0 = py(0.78)
plan.append(f'<rect x="{pxx0:.1f}" y="{pxy0:.1f}" width="{pxw:.1f}" height="{pxh:.1f}" fill="#e3f2fd" stroke="#0277bd" stroke-width="1.6" stroke-dasharray="7,2" rx="5"/>')
plan.append(txt(pxx0 + pxw/2, pxy0 + 17, "PX DEVICE", fs=9, bold=True, fill="#01579b"))
plan.append(txt(pxx0 + pxw/2, pxy0 + 30, "E-01", fs=8.5, fill="#0277bd"))
plan.append(txt(pxx0 + pxw/2, pxy0 + 43, "η = 96%", fs=8, fill="#0277bd"))
plan.append(txt(pxx0 + pxw/2, pxy0 + 55, "ERI PX-70", fs=7.5, fill="#0277bd"))
plan.append(txt(pxx0 + pxw/2, pxy0 + 66, "isobaric rotary", fs=7, fill="#0277bd"))

# ── Seawater inlet arrow ─────────────────────────────────────────────────────
sw_y = py(1.52)
plan.append(f'<line x1="{CX0-40:.1f}" y1="{sw_y:.1f}" x2="{CX0:.1f}" y2="{sw_y:.1f}" stroke="#1565c0" stroke-width="4" marker-end="url(#aC)"/>')
plan.append(txt(CX0-20, sw_y - 12, "SW IN", fs=7.5, bold=True, fill="#1565c0"))
plan.append(txt(CX0-20, sw_y + 2,  "44.4 m³/d", fs=7, fill="#1565c0"))
plan.append(txt(CX0-20, sw_y + 13, "35 g/L NaCl", fs=6.5, fill="#1565c0"))

# Feed flow pipes
plan.append(f'<line x1="{CX0:.1f}" y1="{sw_y:.1f}" x2="{p01x-22:.1f}" y2="{sw_y:.1f}" stroke="#1565c0" stroke-width="3" marker-end="url(#aC)"/>')
plan.append(f'<line x1="{p01x+22:.1f}" y1="{sw_y:.1f}" x2="{ufx0:.1f}" y2="{sw_y:.1f}" stroke="#1565c0" stroke-width="3" marker-end="url(#aC)"/>')
plan.append(f'<line x1="{ufx0+ufw:.1f}" y1="{sw_y:.1f}" x2="{p02x-26:.1f}" y2="{sw_y:.1f}" stroke="#1565c0" stroke-width="3" marker-end="url(#aC)"/>')

# HP pipe (bold double) → RO inlet
hp_label_x = px(3.85)
hp_label_y = py(1.4)
plan.append(f'<line x1="{p02x+26:.1f}" y1="{p02y:.1f}" x2="{px(4.5):.1f}" y2="{p02y:.1f}" stroke="#1565c0" stroke-width="6" marker-end="url(#aC)"/>')
plan.append(f'<rect x="{px(3.5):.1f}" y="{hp_label_y:.1f}" width="{0.7*PPM:.1f}" height="{0.16*PPM:.1f}" fill="#c62828" rx="3"/>')
plan.append(txt(hp_label_x, hp_label_y + 0.1*PPM, "HP 60 bar →", fs=7, bold=True, fill="white"))

# ── RO vessel V-01 ────────────────────────────────────────────────────────────
ro_top = py(1.05)
ro_bot = py(1.39)
ro_h = ro_bot - ro_top
ro_cx = (px(4.5) + px(11.0)) / 2
plan.append(f'<rect x="{px(4.5):.1f}" y="{ro_top:.1f}" width="{6.5*PPM:.1f}" height="{ro_h:.1f}" fill="#bbdefb" stroke="#1565c0" stroke-width="2.2" rx="9"/>')
plan.append(f'<ellipse cx="{px(4.5):.1f}" cy="{py(1.22):.1f}" rx="8" ry="{ro_h/2:.1f}" fill="#1565c0"/>')
plan.append(f'<ellipse cx="{px(11.0):.1f}" cy="{py(1.22):.1f}" rx="8" ry="{ro_h/2:.1f}" fill="#1565c0"/>')
# label split into 2 lines inside the vessel
plan.append(txt(ro_cx, ro_top + 10, "V-01 — RO PRESSURE VESSEL", fs=9, bold=True, fill="#0d47a1"))
plan.append(txt(ro_cx, ro_top + 22, "6 × Filmtec SW30XHR-400i  |  8\" dia. (203 mm OD)  |  6 × 1016 mm elements  |  6.5 m total", fs=7, fill="#1565c0"))
plan.append(txt(ro_cx, ro_top + 33, "Active area: 223 m²  |  Flux J = 20 LMH  |  CP = 1.49  |  NDP = 17.7 bar  |  Recovery 45%", fs=7, fill="#1565c0"))

# Instruments above RO vessel
plan.append(inst(px(5.0),  ro_top - 14, "PI-01", px(5.0),  ro_top))
plan.append(inst(px(6.0),  ro_top - 14, "PT-03", px(6.0),  ro_top))
plan.append(inst(px(9.5),  ro_top - 14, "PI-02", px(9.5),  ro_top))

# ── Permeate run ──────────────────────────────────────────────────────────────
perm_collect_y = py(0.62)
plan.append(f'<line x1="{ro_cx:.1f}" y1="{ro_top:.1f}" x2="{ro_cx:.1f}" y2="{perm_collect_y:.1f}" stroke="#2e7d32" stroke-width="3" marker-end="url(#aG)"/>')
plan.append(inst(ro_cx - 72, perm_collect_y - 12, "FI-02", ro_cx - 72, perm_collect_y))
plan.append(inst(ro_cx,      perm_collect_y - 12, "AT-02", ro_cx,      perm_collect_y))
plan.append(f'<line x1="{ro_cx:.1f}" y1="{perm_collect_y:.1f}" x2="{px(11.0):.1f}" y2="{perm_collect_y:.1f}" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#aG)"/>')
plan.append(txt((ro_cx + px(11.0))/2, perm_collect_y - 6, "20,000 L/day freshwater permeate →", fs=8, fill="#1b5e20"))

# ── Permeate tank T-01 ────────────────────────────────────────────────────────
t01x, t01w = px(11.05), 1.0 * PPM
t01h = 1.15 * PPM
t01y = py(0.14)
plan.append(f'<rect x="{t01x:.1f}" y="{t01y:.1f}" width="{t01w:.1f}" height="{t01h:.1f}" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.6" rx="4"/>')
plan.append(txt(t01x + t01w/2, t01y + 18, "T-01", fs=9.5, bold=True, fill="#1b5e20"))
plan.append(txt(t01x + t01w/2, t01y + 32, "PERMEATE", fs=8.5, fill="#1b5e20"))
plan.append(txt(t01x + t01w/2, t01y + 45, "TANK", fs=8.5, fill="#1b5e20"))
plan.append(txt(t01x + t01w/2, t01y + 60, "20,000 L/d", fs=8, fill="#2e7d32"))
plan.append(txt(t01x + t01w/2, t01y + 73, "&lt;500 ppm TDS", fs=7.5, fill="#2e7d32"))
plan.append(inst(t01x + 14, t01y - 14, "LI-01", t01x + 14, t01y))

# ── Brine flows ───────────────────────────────────────────────────────────────
brine_y = py(1.22)
# from RO → right
plan.append(f'<line x1="{px(11.0):.1f}" y1="{brine_y:.1f}" x2="{t01x+t01w+4:.1f}" y2="{brine_y:.1f}" stroke="#bf5600" stroke-width="4.5" marker-end="url(#aO)"/>')
# down and left back to PX
loop_y = CY0 + CH + 32
plan.append(f'<line x1="{t01x+t01w/2:.1f}" y1="{brine_y:.1f}" x2="{t01x+t01w/2:.1f}" y2="{loop_y:.1f}" stroke="#bf5600" stroke-width="2"/>')
plan.append(f'<line x1="{t01x+t01w/2:.1f}" y1="{loop_y:.1f}" x2="{pxx0+pxw/2:.1f}" y2="{loop_y:.1f}" stroke="#bf5600" stroke-width="2" marker-end="url(#aO)"/>')
plan.append(txt((t01x+t01w/2 + pxx0+pxw/2)/2, loop_y - 5,
               "← brine → PX energy recovery  |  24,400 L/d @ 63.6 g/L  |  high-pressure side", fs=7.5, fill="#bf5600"))
# PX return to HP suction
plan.append(f'<line x1="{pxx0:.1f}" y1="{py(1.52):.1f}" x2="{p02x+26:.1f}" y2="{py(1.52):.1f}" stroke="#0277bd" stroke-width="2" stroke-dasharray="6,2" marker-end="url(#aC)"/>')
plan.append(txt((pxx0 + p02x+26)/2, py(1.44), "PX → HP suction", fs=7, fill="#0277bd"))
# brine discharge
brine_discharge_x = t01x + t01w + 42
plan.append(f'<line x1="{t01x+t01w+4:.1f}" y1="{brine_y:.1f}" x2="{brine_discharge_x:.1f}" y2="{brine_y:.1f}" stroke="#bf5600" stroke-width="3" marker-end="url(#aO)"/>')
plan.append(txt(brine_discharge_x + 6, brine_y - 8, "BRINE OUT", fs=7.5, bold=True, fill="#bf5600", anchor="start"))
plan.append(txt(brine_discharge_x + 6, brine_y + 5,  "63.6 g/L", fs=7, fill="#bf5600", anchor="start"))

# ── Dimension lines ────────────────────────────────────────────────────────────
dim1_y = CY0 + CH + 52
dim2_y = CY0 + CH + 68
plan.append(hdim(px(0), dim1_y, px(12.19), "12.19 m  (container overall length)", col="#333", fs=8.5))
plan.append(hdim(px(0),   dim2_y, px(2.0),   "2.0 m (Zone A)", col="#4527a0"))
plan.append(hdim(px(2.0), dim2_y, px(4.5),   "2.5 m (Zone B)", col="#c62828"))
plan.append(hdim(px(4.5), dim2_y, px(11.0),  "6.5 m — RO vessel zone", col="#1565c0"))
plan.append(hdim(px(11.0), dim2_y, px(12.19), "1.2 m (Zone D)", col="#2e7d32"))
plan.append(vdim(CX0 - 58, CY0, CY0 + CH, "2.44 m (container width)", col="#333", fs=8.5))
plan.append(hdim(px(4.5), CY0 - 32, px(11.0), '6 × 1016 mm elements — Filmtec SW30XHR-400i  (8" OD)', col="#1565c0", fs=7.5))

# ── Legend ────────────────────────────────────────────────────────────────────
lg_y = H - 44 - 70
plan.append(f'<rect x="14" y="{lg_y:.1f}" width="460" height="62" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
plan.append(txt(244, lg_y + 13, "FLOW LEGEND", fs=9, bold=True, fill="#333"))
plan.append(f'<line x1="24" y1="{lg_y+28:.1f}" x2="68" y2="{lg_y+28:.1f}" stroke="#1565c0" stroke-width="4"/>')
plan.append(txt(73, lg_y + 32, "Feed / HP seawater (process pipe)", fs=8, fill="#333", anchor="start"))
plan.append(f'<line x1="24" y1="{lg_y+48:.1f}" x2="68" y2="{lg_y+48:.1f}" stroke="#2e7d32" stroke-width="4"/>')
plan.append(txt(73, lg_y + 52, "Permeate — freshwater product", fs=8, fill="#333", anchor="start"))
plan.append(f'<line x1="250" y1="{lg_y+28:.1f}" x2="294" y2="{lg_y+28:.1f}" stroke="#bf5600" stroke-width="4"/>')
plan.append(txt(299, lg_y + 32, "Brine reject  (24,400 L/d, 63.6 g/L)", fs=8, fill="#333", anchor="start"))
plan.append(f'<line x1="250" y1="{lg_y+48:.1f}" x2="294" y2="{lg_y+48:.1f}" stroke="#ad1457" stroke-width="1.5" stroke-dasharray="5,2"/>')
plan.append(txt(299, lg_y + 52, "Chemical dosing (dashed)", fs=8, fill="#333", anchor="start"))

# Design basis box
plan.append(f'<rect x="488" y="{lg_y:.1f}" width="696" height="62" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
plan.append(txt(836, lg_y + 13, "DESIGN BASIS", fs=9, bold=True, fill="#333"))
plan.append(txt(496, lg_y + 28, "Output: 20,000 L/d  |  Feed: 44.4 m³/d  |  Recovery: 45%  |  Brine: 24.4 m³/d  |  TDS reject >99.75%", fs=7.5, fill="#333", anchor="start"))
plan.append(txt(496, lg_y + 42, "π_feed = 28.4 bar (van't Hoff)  |  ΔP = 60 bar  |  CP = 1.49  |  π_membrane = 42.3 bar  |  NDP = 17.7 bar", fs=7.5, fill="#333", anchor="start"))
plan.append(txt(496, lg_y + 56, "SEC = 3.5 kWh/m³ (with PX η=96%)  |  E_day = 70 kWh  |  LFP battery = 87.5 kWh  |  PV = 14.8 kWp", fs=7.5, fill="#333", anchor="start"))

plan.append(title_block("ARCH-R2-CAD-001", "SOLAR SPRO SYSTEM — PLAN VIEW (TOP)", "Scale 1:60  |  40 ft ISO Container  |  All dims in metres", "1:60"))

with open("deliverables/02_cad_concept/01_plan_view.svg", "w") as f:
    f.write(svg_wrap("".join(plan)))
print("01_plan_view.svg OK")


# ════════════════════════════════════════════════════════════════════════════
# 2. FRONT ELEVATION  (side view, 1:50)
# Container: 12.19 m (L) × 2.59 m (H)
# ════════════════════════════════════════════════════════════════════════════
PPE = 58.0           # px per metre
EX0, EY0 = 90, 72   # container top-left corner
EW = 12.19 * PPE    # ≈ 707 px
EH = 2.59 * PPE     # ≈ 150 px


def ex(m): return EX0 + m * PPE
def ey(m): return EY0 + m * PPE   # downward from roof


elev = []
elev.append(txt(W/2, 26, "FRONT ELEVATION (SIDE VIEW) — SOLAR-POWERED SWRO  20,000 L/DAY", fs=13, bold=True, fill="#1a3a6b"))
elev.append(txt(W/2, 42, "Scale 1:50  |  40 ft ISO Container  |  All dimensions in metres  |  Ground line shown", fs=9, fill="#555"))

# Container body
elev.append(f'<rect x="{EX0:.1f}" y="{EY0:.1f}" width="{EW:.1f}" height="{EH:.1f}" fill="#f8faff" stroke="#1a3a6b" stroke-width="2.5"/>')
# Structural corner posts
for xi in [EX0, EX0 + EW - 5]:
    elev.append(f'<rect x="{xi:.1f}" y="{EY0:.1f}" width="5" height="{EH:.1f}" fill="#2c3e50"/>')
# Top/bottom rails
elev.append(f'<rect x="{EX0:.1f}" y="{EY0:.1f}" width="{EW:.1f}" height="5.5" fill="#1a3a6b"/>')
elev.append(f'<rect x="{EX0:.1f}" y="{EY0+EH-5.5:.1f}" width="{EW:.1f}" height="5.5" fill="#1a3a6b"/>')
# Ground line
gl_y = EY0 + EH
elev.append(f'<line x1="{EX0-30:.1f}" y1="{gl_y:.1f}" x2="{EX0+EW+30:.1f}" y2="{gl_y:.1f}" stroke="#666" stroke-width="2" stroke-dasharray="10,5"/>')
elev.append(txt(EX0 - 20, gl_y + 12, "G.L.", fs=8.5, fill="#666"))

# PV panels on roof (tilted 15° south)
panel_y = EY0 - 40
elev.append(f'<rect x="{EX0+18:.1f}" y="{panel_y:.1f}" width="{EW-36:.1f}" height="28" fill="#1e3a6b" stroke="#2980b9" stroke-width="1.3" rx="3"/>')
# Panel grid lines
for i in range(1, 9):
    gx = EX0 + 18 + i * (EW-36) / 9
    elev.append(f'<line x1="{gx:.1f}" y1="{panel_y:.1f}" x2="{gx:.1f}" y2="{panel_y+28:.1f}" stroke="#2980b9" stroke-width="0.5" opacity="0.5"/>')
elev.append(txt(EX0 + EW/2, panel_y + 18, "PV ARRAY — 37 × 400 W  |  14.8 kWp  |  72.9 m²  |  15° fixed tilt south  |  η = 21%", fs=8, bold=True, fill="#aed6f1"))
# Tilt angle indicator
elev.append(f'<line x1="{EX0+32:.1f}" y1="{EY0:.1f}" x2="{EX0+80:.1f}" y2="{panel_y+28:.1f}" stroke="#f39c12" stroke-width="1.2"/>')
elev.append(txt(EX0 + 58, EY0 - 5, "15°", fs=7.5, fill="#f39c12"))

# Louvres (ventilation, both ends)
for lx in [ex(0.22), ex(10.88)]:
    lvw, lvh = 0.72 * PPE, 0.35 * PPE
    elev.append(f'<rect x="{lx:.1f}" y="{ey(0.25):.1f}" width="{lvw:.1f}" height="{lvh:.1f}" fill="#d0d0d0" stroke="#888" stroke-width="0.9" rx="2"/>')
    for n in range(4):
        ly2 = ey(0.25) + 5 + n * (lvh - 5) / 4
        elev.append(f'<line x1="{lx+2:.1f}" y1="{ly2:.1f}" x2="{lx+lvw-2:.1f}" y2="{ly2:.1f}" stroke="#aaa" stroke-width="1.2"/>')
    elev.append(txt(lx + lvw/2, ey(0.25) + lvh + 12, "LOUVRE", fs=7, fill="#666"))

# Door (outlet end)
door_x = ex(11.1)
door_w, door_h = 0.75 * PPE, 1.55 * PPE
door_y = ey(1.0)
elev.append(f'<rect x="{door_x:.1f}" y="{door_y:.1f}" width="{door_w:.1f}" height="{door_h:.1f}" fill="#b0bec5" stroke="#607d8b" stroke-width="1.3"/>')
elev.append(f'<line x1="{door_x:.1f}" y1="{door_y:.1f}" x2="{door_x+door_w:.1f}" y2="{door_y+door_h:.1f}" stroke="#607d8b" stroke-width="0.6"/>')
elev.append(txt(door_x + door_w/2, door_y + door_h/2, "DOOR", fs=8, fill="#37474f"))

# Battery bank (dashed, inside top zone)
bat_h = 0.68 * PPE
elev.append(f'<rect x="{ex(0.12):.1f}" y="{ey(0.08):.1f}" width="{3.9*PPE:.1f}" height="{bat_h:.1f}" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.3" stroke-dasharray="6,2" rx="3"/>')
elev.append(txt(ex(2.07), ey(0.08) + bat_h*0.38, "LFP BATTERY — BAT-01  |  87.5 kWh  |  H ≈ 0.65 m", fs=8.5, bold=True, fill="#1b5e20"))
elev.append(txt(ex(2.07), ey(0.08) + bat_h*0.70, "4 racks × 1.0 m  |  mounted 0.10 m above floor  |  CATL 280 Ah  |  48 V", fs=7.5, fill="#2e7d32"))

# UF skid
uf_w, uf_h = 1.55 * PPE, 1.65 * PPE
elev.append(f'<rect x="{ex(0.08):.1f}" y="{ey(0.90):.1f}" width="{uf_w:.1f}" height="{uf_h:.1f}" fill="#ede7f6" stroke="#5c35cc" stroke-width="1.6" stroke-dasharray="6,2" rx="4"/>')
elev.append(txt(ex(0.08) + uf_w/2, ey(0.90) + uf_h*0.32, "UF PRE-TX", fs=8.5, bold=True, fill="#4527a0"))
elev.append(txt(ex(0.08) + uf_w/2, ey(0.90) + uf_h*0.50, "F-01", fs=8, fill="#512da8"))
elev.append(txt(ex(0.08) + uf_w/2, ey(0.90) + uf_h*0.66, "0.02 µm PVDF", fs=7.5, fill="#5c35cc"))
elev.append(txt(ex(0.08) + uf_w/2, ey(0.90) + uf_h*0.80, "H = 1.6 m | W = 1.5 m", fs=7, fill="#5c35cc"))

# Pumps
# P-01 LP
elev.append(f'<ellipse cx="{ex(1.85):.1f}" cy="{ey(2.32):.1f}" rx="22" ry="15" fill="#fff8e1" stroke="#f57f17" stroke-width="1.8"/>')
elev.append(txt(ex(1.85), ey(2.30), "P-01", fs=8, bold=True, fill="#e65100"))
elev.append(txt(ex(1.85), ey(2.41), "LP", fs=7, fill="#e65100"))
# P-02 HP
elev.append(f'<ellipse cx="{ex(2.85):.1f}" cy="{ey(2.30):.1f}" rx="24" ry="18" fill="#ffebee" stroke="#c62828" stroke-width="2.2"/>')
elev.append(txt(ex(2.85), ey(2.27), "P-02", fs=8.5, bold=True, fill="#b71c1c"))
elev.append(txt(ex(2.85), ey(2.38), "HP 60 bar", fs=7.5, fill="#c62828"))

# PX device
px_bx0, px_bw = ex(3.3), 0.9 * PPE
px_bh = 0.75 * PPE
px_by0 = ey(1.62)
elev.append(f'<rect x="{px_bx0:.1f}" y="{px_by0:.1f}" width="{px_bw:.1f}" height="{px_bh:.1f}" fill="#e3f2fd" stroke="#0277bd" stroke-width="1.3" stroke-dasharray="5,2" rx="4"/>')
elev.append(txt(px_bx0 + px_bw/2, px_by0 + px_bh*0.38, "PX — E-01", fs=8.5, bold=True, fill="#01579b"))
elev.append(txt(px_bx0 + px_bw/2, px_by0 + px_bh*0.60, "η = 96%", fs=8, fill="#0277bd"))
elev.append(txt(px_bx0 + px_bw/2, px_by0 + px_bh*0.80, "ERI PX-70", fs=7, fill="#0277bd"))

# RO vessel (horizontal cylinder) — CL at 0.68 m from floor
ro_cl_e = EY0 + (2.59 - 0.68) * PPE
ro_re = 0.115 * PPE    # radius from 203 mm OD
ro_x1_e = ex(4.5)
ro_x2_e = ex(11.0)
elev.append(f'<rect x="{ro_x1_e:.1f}" y="{ro_cl_e-ro_re:.1f}" width="{ro_x2_e-ro_x1_e:.1f}" height="{2*ro_re:.1f}" fill="#bbdefb" stroke="#1565c0" stroke-width="2.2" rx="8"/>')
elev.append(f'<ellipse cx="{ro_x1_e:.1f}" cy="{ro_cl_e:.1f}" rx="8" ry="{ro_re:.1f}" fill="#1565c0"/>')
elev.append(f'<ellipse cx="{ro_x2_e:.1f}" cy="{ro_cl_e:.1f}" rx="8" ry="{ro_re:.1f}" fill="#1565c0"/>')
for i in range(1, 6):
    xd = ro_x1_e + i * (ro_x2_e - ro_x1_e) / 6
    elev.append(f'<line x1="{xd:.1f}" y1="{ro_cl_e-ro_re:.1f}" x2="{xd:.1f}" y2="{ro_cl_e+ro_re:.1f}" stroke="#1565c0" stroke-width="0.9" opacity="0.5"/>')
elev.append(txt((ro_x1_e+ro_x2_e)/2, ro_cl_e - 3, "V-01 — RO PRESSURE VESSEL", fs=8.5, bold=True, fill="#0d47a1"))
elev.append(txt((ro_x1_e+ro_x2_e)/2, ro_cl_e + 8, "6 × Filmtec SW30XHR-400i  |  8\" OD (203 mm)  |  CL at +680 mm from floor", fs=7.5, fill="#1565c0"))

# Saddle supports
for sx in [ex(5.0), ex(7.75), ex(10.5)]:
    sup_h = EY0 + EH - ro_cl_e - ro_re
    elev.append(f'<rect x="{sx-11:.1f}" y="{ro_cl_e+ro_re:.1f}" width="22" height="{sup_h:.1f}" fill="#607d8b"/>')
    elev.append(f'<rect x="{sx-19:.1f}" y="{EY0+EH-9:.1f}" width="38" height="9" fill="#455a64"/>')
elev.append(txt(ex(5.0), EY0+EH-3.5, "SADDLE", fs=6.5, fill="white"))

# HP feed pipe
hp_e_y = ro_cl_e
elev.append(f'<line x1="{ex(1.6):.1f}" y1="{hp_e_y:.1f}" x2="{ro_x1_e:.1f}" y2="{hp_e_y:.1f}" stroke="#1565c0" stroke-width="5.5" marker-end="url(#aC)"/>')
elev.append(f'<rect x="{ex(2.4):.1f}" y="{hp_e_y-6:.1f}" width="{1.0*PPE:.1f}" height="12" fill="#c62828" rx="2"/>')
elev.append(txt(ex(2.9), hp_e_y + 4, "HP 60 bar →", fs=7.5, bold=True, fill="white"))

# Permeate collect header
perm_ey = ro_cl_e - ro_re - 22
elev.append(f'<line x1="{(ro_x1_e+ro_x2_e)/2:.1f}" y1="{ro_cl_e-ro_re:.1f}" x2="{(ro_x1_e+ro_x2_e)/2:.1f}" y2="{perm_ey:.1f}" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#aG)"/>')
elev.append(f'<line x1="{(ro_x1_e+ro_x2_e)/2:.1f}" y1="{perm_ey:.1f}" x2="{ex(11.15):.1f}" y2="{perm_ey:.1f}" stroke="#2e7d32" stroke-width="2.2" marker-end="url(#aG)"/>')
elev.append(txt((ro_x1_e+ro_x2_e)/2 + 60, perm_ey - 5, "permeate  20,000 L/d", fs=8, fill="#1b5e20"))

# Permeate tank T-01
t01e_x = ex(11.15)
t01e_w = 0.9 * PPE
t01e_y = EY0 + 0.85 * PPE
t01e_h = 1.65 * PPE
elev.append(f'<rect x="{t01e_x:.1f}" y="{t01e_y:.1f}" width="{t01e_w:.1f}" height="{t01e_h:.1f}" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.6" rx="4"/>')
elev.append(txt(t01e_x + t01e_w/2, t01e_y + t01e_h*0.30, "T-01", fs=9, bold=True, fill="#1b5e20"))
elev.append(txt(t01e_x + t01e_w/2, t01e_y + t01e_h*0.48, "PERMEATE", fs=8, fill="#1b5e20"))
elev.append(txt(t01e_x + t01e_w/2, t01e_y + t01e_h*0.63, "H = 1.6 m", fs=7.5, fill="#2e7d32"))
elev.append(txt(t01e_x + t01e_w/2, t01e_y + t01e_h*0.78, "20,000 L/d", fs=7.5, fill="#2e7d32"))
elev.append(txt(t01e_x + t01e_w/2, t01e_y + t01e_h*0.92, "&lt;500 ppm", fs=7, fill="#2e7d32"))

# Brine pipe
elev.append(f'<line x1="{ro_x2_e:.1f}" y1="{ro_cl_e:.1f}" x2="{t01e_x+t01e_w:.1f}" y2="{ro_cl_e:.1f}" stroke="#bf5600" stroke-width="3" marker-end="url(#aO)"/>')
elev.append(txt(t01e_x + t01e_w + 6, ro_cl_e - 5, "BRINE OUT", fs=8, bold=True, fill="#bf5600", anchor="start"))

# Dimension lines
dim1_y_e = EY0 + EH + 30
dim2_y_e = EY0 + EH + 48
elev.append(hdim(EX0, dim1_y_e, EX0 + EW, "12.19 m  (container overall length)", col="#333", fs=8.5))
elev.append(hdim(ro_x1_e, dim2_y_e, ro_x2_e, "6.5 m  (RO vessel zone)", col="#1565c0", fs=8))
elev.append(vdim(EX0 - 58, EY0, EY0 + EH, "2.59 m  (container height)", col="#333", fs=8.5))
elev.append(vdim(EX0 - 38, EY0 + EH, ro_cl_e, "0.68 m  CL", col="#1565c0", fs=7.5))
elev.append(vdim(ro_x2_e + 52, ro_cl_e - ro_re, ro_cl_e + ro_re, "203 mm OD", col="#1565c0", fs=7))

# Height reference ticks
for (ry_ref, lbl, col_r) in [(EY0, "+2590 mm (roof)", "#333"), (ro_cl_e, "+680 mm (RO vessel CL)", "#1565c0"), (gl_y, "±0 mm (floor / G.L.)", "#666")]:
    elev.append(f'<line x1="{EX0+EW+10:.1f}" y1="{ry_ref:.1f}" x2="{EX0+EW+32:.1f}" y2="{ry_ref:.1f}" stroke="{col_r}" stroke-width="0.9"/>')
    elev.append(txt(EX0+EW+35, ry_ref + 3.5, lbl, fs=7.5, fill=col_r, anchor="start"))

# Notes
note_y = H - 44 - 75
elev.append(f'<rect x="14" y="{note_y:.1f}" width="{W-28}" height="67" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
elev.append(txt(W/2, note_y + 13, "CONSTRUCTION NOTES", fs=9, bold=True, fill="#333"))
elev.append(txt(22, note_y + 27, "1. HP piping: DN50 seamless SS316L, PN 100 bar, butt-welded. LP piping: DN80 HDPE PE100 PN10 flanged.", fs=8, fill="#333", anchor="start"))
elev.append(txt(22, note_y + 41, "2. Vessel saddle supports: SS304 formed saddle, grouted baseplate, 3 off at 5.0 m, 7.75 m, 10.5 m from inlet end.", fs=8, fill="#333", anchor="start"))
elev.append(txt(22, note_y + 55, "3. Container: 40 ft ISO Corten steel, galvanised interior. Louvres: 700 × 350 mm stainless mesh, both ends. Door: outlet end.", fs=8, fill="#333", anchor="start"))

elev.append(title_block("ARCH-R2-CAD-002", "SOLAR SPRO SYSTEM — FRONT ELEVATION (SIDE VIEW)", "Scale 1:50  |  40 ft ISO Container  |  All dims in mm unless noted", "1:50"))

with open("deliverables/02_cad_concept/02_front_elevation.svg", "w") as f:
    f.write(svg_wrap("".join(elev)))
print("02_front_elevation.svg OK")


# ════════════════════════════════════════════════════════════════════════════
# 3. END ELEVATION  (inlet face, 1:20)
# Container end wall: 2.44 m W × 2.59 m H
# ════════════════════════════════════════════════════════════════════════════
PPF = 150.0        # px per metre (1:20 scale)
FW = 2.44 * PPF   # 366 px
FH = 2.59 * PPF   # 388.5 px
FX0 = (W - FW) / 2   # centred horizontally  ≈ 417
FY0 = 62.0


def fx(m): return FX0 + m * PPF
def fy(m): return FY0 + m * PPF


end = []
end.append(txt(W/2, 26, "END ELEVATION (INLET FACE) — SOLAR-POWERED SWRO  20,000 L/DAY", fs=13, bold=True, fill="#1a3a6b"))
end.append(txt(W/2, 42, "Scale 1:20  |  Inlet (west) End of 40 ft ISO Container  |  All dimensions in metres", fs=9, fill="#555"))

# Container face
end.append(f'<rect x="{FX0:.1f}" y="{FY0:.1f}" width="{FW:.1f}" height="{FH:.1f}" fill="#f8faff" stroke="#1a3a6b" stroke-width="2.5"/>')
# Corner posts
for xi_f in [FX0, FX0 + FW - 9]:
    end.append(f'<rect x="{xi_f:.1f}" y="{FY0:.1f}" width="9" height="{FH:.1f}" fill="#2c3e50"/>')
# Rails
end.append(f'<rect x="{FX0:.1f}" y="{FY0:.1f}" width="{FW:.1f}" height="7" fill="#1a3a6b"/>')
end.append(f'<rect x="{FX0:.1f}" y="{FY0+FH-7:.1f}" width="{FW:.1f}" height="7" fill="#1a3a6b"/>')
# Ground line
end.append(f'<line x1="{FX0-25:.1f}" y1="{FY0+FH:.1f}" x2="{FX0+FW+25:.1f}" y2="{FY0+FH:.1f}" stroke="#666" stroke-width="2" stroke-dasharray="8,4"/>')
end.append(txt(FX0 - 18, FY0 + FH + 13, "G.L.", fs=9, fill="#666"))

# PV panels (edge-on profile, 15° tilt)
end.append(f'<line x1="{FX0+22:.1f}" y1="{FY0-10:.1f}" x2="{FX0+FW-22:.1f}" y2="{FY0-38:.1f}" stroke="#1e3a6b" stroke-width="5"/>')
end.append(txt(FX0 + FW/2, FY0 - 44, "PV PANELS (edge-on, 15° tilt south)  |  37 × 400 W = 14.8 kWp", fs=8.5, fill="#1e3a6b"))
# Tilt arc
end.append(f'<path d="M {FX0+22:.1f} {FY0-10:.1f} A 28 28 0 0 0 {FX0+50:.1f} {FY0-10:.1f}" stroke="#f39c12" fill="none" stroke-width="1.2"/>')
end.append(txt(FX0 + 38, FY0 - 5, "15°", fs=8, fill="#f39c12"))

# SW inlet pipe (lower left, DN80)
pipe_y = fy(2.59 - 0.50)
end.append(f'<circle cx="{FX0:.1f}" cy="{pipe_y:.1f}" r="10" fill="#1565c0" stroke="#0d47a1" stroke-width="1.8"/>')
end.append(f'<circle cx="{FX0:.1f}" cy="{pipe_y:.1f}" r="4" fill="white"/>')
end.append(txt(FX0 - 12, pipe_y - 14, "SW INLET →", fs=8.5, bold=True, fill="#1565c0", anchor="end"))
end.append(txt(FX0 - 12, pipe_y,      "44.4 m³/day", fs=8, fill="#1565c0", anchor="end"))
end.append(txt(FX0 - 12, pipe_y + 13, "DN80 SS316L", fs=7.5, fill="#1565c0", anchor="end"))
end.append(txt(FX0 - 12, pipe_y + 25, "PN10 flanged", fs=7, fill="#1565c0", anchor="end"))

# Cable conduit (lower right)
end.append(f'<circle cx="{FX0+FW:.1f}" cy="{fy(2.59-0.3):.1f}" r="7" fill="#333" stroke="#222" stroke-width="1.2"/>')
end.append(txt(FX0 + FW + 14, fy(2.59-0.3) + 3, "DC cable", fs=7.5, fill="#333", anchor="start"))
end.append(txt(FX0 + FW + 14, fy(2.59-0.3) + 14, "conduit", fs=7.5, fill="#333", anchor="start"))

# UF skid (left interior, dashed)
uf_f_x = fx(0.10)
uf_f_w = 1.05 * PPF
uf_f_y = fy(0.88)
uf_f_h = 1.60 * PPF
end.append(f'<rect x="{uf_f_x:.1f}" y="{uf_f_y:.1f}" width="{uf_f_w:.1f}" height="{uf_f_h:.1f}" fill="#ede7f6" stroke="#5c35cc" stroke-width="1.8" stroke-dasharray="9,3" rx="5"/>')
end.append(txt(uf_f_x + uf_f_w/2, uf_f_y + uf_f_h*0.28, "UF PRE-TX", fs=10, bold=True, fill="#4527a0"))
end.append(txt(uf_f_x + uf_f_w/2, uf_f_y + uf_f_h*0.43, "F-01", fs=9.5, fill="#512da8"))
end.append(txt(uf_f_x + uf_f_w/2, uf_f_y + uf_f_h*0.56, "0.02 µm PVDF", fs=8.5, fill="#5c35cc"))
end.append(txt(uf_f_x + uf_f_w/2, uf_f_y + uf_f_h*0.68, "Hollow fibre", fs=8, fill="#5c35cc"))
end.append(txt(uf_f_x + uf_f_w/2, uf_f_y + uf_f_h*0.79, "SDI &lt;3", fs=8, fill="#5c35cc"))
end.append(txt(uf_f_x + uf_f_w/2, uf_f_y + uf_f_h*0.90, "W × H: 1.05 × 1.60 m", fs=7.5, fill="#5c35cc"))

# LP pump P-01
p01f_cx = fx(1.75)
p01f_cy = fy(2.36)
end.append(f'<circle cx="{p01f_cx:.1f}" cy="{p01f_cy:.1f}" r="30" fill="#fff8e1" stroke="#f57f17" stroke-width="2.2"/>')
end.append(txt(p01f_cx, p01f_cy - 6,  "P-01", fs=10, bold=True, fill="#e65100"))
end.append(txt(p01f_cx, p01f_cy + 8,  "LP | 2.5 bar", fs=8.5, fill="#e65100"))
end.append(txt(p01f_cx, p01f_cy + 20, "1.85 m³/h", fs=7.5, fill="#e65100"))

# Battery (top zone)
bat_f_x = fx(0.07)
bat_f_w = 2.30 * PPF
bat_f_y = fy(0.07)
bat_f_h = 0.65 * PPF
end.append(f'<rect x="{bat_f_x:.1f}" y="{bat_f_y:.1f}" width="{bat_f_w:.1f}" height="{bat_f_h:.1f}" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.8" stroke-dasharray="8,3" rx="4"/>')
end.append(txt(bat_f_x + bat_f_w/2, bat_f_y + bat_f_h*0.35, "LFP BATTERY — BAT-01", fs=10, bold=True, fill="#1b5e20"))
end.append(txt(bat_f_x + bat_f_w/2, bat_f_y + bat_f_h*0.60, "87.5 kWh  |  48 V  |  4 racks", fs=9, fill="#2e7d32"))
end.append(txt(bat_f_x + bat_f_w/2, bat_f_y + bat_f_h*0.82, "W × H: 2.30 × 0.65 m", fs=8.5, fill="#2e7d32"))

# Inverter (right zone)
inv_f_x = fx(1.60)
inv_f_w = 0.76 * PPF
inv_f_y = fy(0.78)
inv_f_h = 0.72 * PPF
end.append(f'<rect x="{inv_f_x:.1f}" y="{inv_f_y:.1f}" width="{inv_f_w:.1f}" height="{inv_f_h:.1f}" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="1.6" stroke-dasharray="7,3" rx="4"/>')
end.append(txt(inv_f_x + inv_f_w/2, inv_f_y + inv_f_h*0.32, "INV-01", fs=10, bold=True, fill="#4a148c"))
end.append(txt(inv_f_x + inv_f_w/2, inv_f_y + inv_f_h*0.53, "Victron 48/8000", fs=8.5, fill="#6a1b9a"))
end.append(txt(inv_f_x + inv_f_w/2, inv_f_y + inv_f_h*0.72, "8 kW AC | MPPT", fs=8, fill="#6a1b9a"))
end.append(txt(inv_f_x + inv_f_w/2, inv_f_y + inv_f_h*0.88, "150V / 100A", fs=7.5, fill="#6a1b9a"))

# RO vessel outline (cross-section, 8" OD = 203 mm)
ro_f_cx = fx(1.22)   # centred in container width
ro_f_r = 0.101 * PPF  # radius 101.5 mm → scaled
ro_f_cy = fy(2.59 - 0.68)
end.append(f'<circle cx="{ro_f_cx:.1f}" cy="{ro_f_cy:.1f}" r="{ro_f_r:.1f}" fill="#bbdefb" stroke="#1565c0" stroke-width="2.2"/>')
end.append(f'<circle cx="{ro_f_cx:.1f}" cy="{ro_f_cy:.1f}" r="{ro_f_r*0.45:.1f}" fill="#e3f2fd" stroke="#1565c0" stroke-width="0.8"/>')  # inner bore
end.append(txt(ro_f_cx, ro_f_cy + ro_f_r + 14, "V-01  8\" OD", fs=8, bold=True, fill="#0d47a1"))
end.append(txt(ro_f_cx, ro_f_cy + ro_f_r + 26, "CL at +680 mm", fs=7.5, fill="#1565c0"))

# Dimension lines
dim_f1 = FY0 + FH + 30
dim_f2 = FY0 + FH + 48
end.append(hdim(FX0, dim_f1, FX0 + FW, "2.44 m  (container internal width)", col="#333", fs=8.5))
end.append(hdim(uf_f_x, dim_f2, uf_f_x + uf_f_w, "1.05 m  (UF skid footprint)", col="#5c35cc", fs=8))
end.append(vdim(FX0 - 60, FY0, FY0 + FH, "2.59 m  (container height)", col="#333", fs=8.5))
end.append(vdim(FX0 - 38, bat_f_y, bat_f_y + bat_f_h, "0.65 m  (battery zone)", col="#2e7d32", fs=7.5))
end.append(vdim(FX0 + FW + 52, uf_f_y, uf_f_y + uf_f_h, "1.60 m  (UF skid)", col="#5c35cc", fs=7.5))
# RO vessel CL dimension
end.append(vdim(FX0 + FW + 78, ro_f_cy - ro_f_r, ro_f_cy + ro_f_r, "203 mm OD", col="#1565c0", fs=7))

# Notes panel
note_fy = H - 44 - 70
end.append(f'<rect x="14" y="{note_fy:.1f}" width="{W-28}" height="62" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
end.append(txt(W/2, note_fy + 13, "NOTES", fs=9, bold=True, fill="#333"))
end.append(txt(22, note_fy + 28, "1. SW inlet flange: DN80 PN10 ANSI 150 flanged, with isolation valve (GV-01) and duplex basket strainer (STR-01) on inlet face.", fs=8, fill="#333", anchor="start"))
end.append(txt(22, note_fy + 42, "2. Permeate outlet and brine discharge exit on the outlet (east) face — see Plan View DWG ARCH-R2-CAD-001.", fs=8, fill="#333", anchor="start"))
end.append(txt(22, note_fy + 56, "3. DC cable conduit (lower right, DN40) carries PV array cabling to inverter INV-01. All electrical in IP65 conduit.", fs=8, fill="#333", anchor="start"))

end.append(title_block("ARCH-R2-CAD-003", "SOLAR SPRO SYSTEM — END ELEVATION (INLET FACE)", "Scale 1:20  |  40 ft ISO Container  |  All dims in metres", "1:20"))

with open("deliverables/02_cad_concept/03_end_elevation.svg", "w") as f:
    f.write(svg_wrap("".join(end)))
print("03_end_elevation.svg OK")


# ════════════════════════════════════════════════════════════════════════════
# 4. ISOMETRIC VIEW
# ════════════════════════════════════════════════════════════════════════════
ISO_SCALE = 48.0
ISO_OX, ISO_OY = 155, 430   # origin (front-left-bottom of container)


def iso(x, y, z):
    """Isometric projection: x=length (m), y=width (m), z=height (m)."""
    ipx = ISO_OX + (x - y) * ISO_SCALE * math.cos(math.radians(30))
    ipy = ISO_OY - (x + y) * ISO_SCALE * math.sin(math.radians(30)) - z * ISO_SCALE
    return ipx, ipy


def iso_line(x1, y1, z1, x2, y2, z2, stroke, sw=1.5, dash=""):
    p1, p2 = iso(x1, y1, z1), iso(x2, y2, z2)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{stroke}" stroke-width="{sw}"{da}/>'


def iso_face(pts_3d, fill, stroke, sw=1.5, dash="", opacity=1.0):
    pts = [iso(x, y, z) for x, y, z in pts_3d]
    pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'<polygon points="{pts_str}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{da}{op}/>'


def iso_txt(x, y, z, s, anchor="middle", fs=8.5, fill="#111", bold=False):
    ipx, ipy = iso(x, y, z)
    fw = ' font-weight="bold"' if bold else ""
    return f'<text x="{ipx:.1f}" y="{ipy:.1f}" text-anchor="{anchor}" font-family="Arial" font-size="{fs}" fill="{fill}"{fw}>{s}</text>'


CL_I, CW_I, CH_I = 12.19, 2.44, 2.59

iso_p = []
iso_p.append(txt(W/2, 26, "ISOMETRIC VIEW — SOLAR-POWERED SWRO DESALINATION SYSTEM — 20,000 L/DAY", fs=13, bold=True, fill="#1a3a6b"))
iso_p.append(txt(W/2, 42, "Scale NTS  |  40 ft ISO Container  |  Viewed from south-east, above  |  Dimensions in metres", fs=9, fill="#555"))

# Ground shadow
shadow = [iso(0,0,0), iso(CL_I,0,0), iso(CL_I,CW_I,0), iso(0,CW_I,0)]
s_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in shadow)
iso_p.append(f'<polygon points="{s_str}" fill="#ccc" opacity="0.25"/>')

# Container faces
iso_p.append(iso_face([(0,0,0),(CL_I,0,0),(CL_I,CW_I,0),(0,CW_I,0)], "#dfe8f5", "#1a3a6b", 1.0, "", 0.35))
iso_p.append(iso_face([(0,0,0),(CL_I,0,0),(CL_I,0,CH_I),(0,0,CH_I)], "#e8f0fb", "#1a3a6b", 2.0))
iso_p.append(iso_face([(CL_I,0,0),(CL_I,CW_I,0),(CL_I,CW_I,CH_I),(CL_I,0,CH_I)], "#d0ddf0", "#1a3a6b", 2.0))
iso_p.append(iso_face([(0,0,CH_I),(CL_I,0,CH_I),(CL_I,CW_I,CH_I),(0,CW_I,CH_I)], "#f4f7ff", "#1a3a6b", 1.5, "6,3", 0.9))
iso_p.append(iso_face([(0,0,0),(0,CW_I,0),(0,CW_I,CH_I),(0,0,CH_I)], "#d8e5f5", "#1a3a6b", 2.0))
iso_p.append(iso_face([(0,CW_I,0),(CL_I,CW_I,0),(CL_I,CW_I,CH_I),(0,CW_I,CH_I)], "#c8d8f0", "#1a3a6b", 1.5, "", 0.7))

# PV panels on roof (2 rows × 14 cols ≈ 28; add 9 in a third partial row)
pv_z = CH_I
for row in range(2):
    for col in range(14):
        pv0x = 0.25 + col * 0.86
        pv0y = 0.18 + row * 1.04
        iso_p.append(iso_face(
            [(pv0x, pv0y, pv_z), (pv0x+0.76, pv0y, pv_z),
             (pv0x+0.76, pv0y+0.90, pv_z), (pv0x, pv0y+0.90, pv_z)],
            "#1e3a6b", "#2980b9", 0.7))
# 9 extra panels third row
for col in range(9):
    pv0x = 0.25 + col * 0.86
    pv0y = 0.18 + 2.08
    iso_p.append(iso_face(
        [(pv0x, pv0y, pv_z), (pv0x+0.76, pv0y, pv_z),
         (pv0x+0.76, pv0y+0.90, pv_z), (pv0x, pv0y+0.90, pv_z)],
        "#1e3a6b", "#2980b9", 0.7))
p_pv = iso(CL_I/2, CW_I/4, CH_I + 0.22)
iso_p.append(f'<text x="{p_pv[0]:.1f}" y="{p_pv[1]:.1f}" text-anchor="middle" font-family="Arial" font-size="9" font-weight="bold" fill="#0d47a1">PV ARRAY — 37 × 400 W  |  14.8 kWp  |  72.9 m²  |  15° tilt south</text>')

# Battery bank (back-top)
iso_p.append(iso_face([(0.12, 1.45, 0.10), (3.95, 1.45, 0.10), (3.95, 2.32, 0.10), (0.12, 2.32, 0.10)], "#e8f5e9", "#2e7d32", 1.2, "5,2", 0.85))
iso_p.append(iso_face([(0.12, 1.45, 0.10), (3.95, 1.45, 0.10), (3.95, 1.45, 0.78), (0.12, 1.45, 0.78)], "#c8e6c9", "#2e7d32", 1.2, "5,2", 0.85))
iso_p.append(iso_face([(3.95, 1.45, 0.10), (3.95, 2.32, 0.10), (3.95, 2.32, 0.78), (3.95, 1.45, 0.78)], "#a5d6a7", "#2e7d32", 1.2, "5,2", 0.85))
iso_p.append(iso_txt(2.0, 1.87, 0.55, "LFP BATTERY — BAT-01  |  87.5 kWh  |  48 V", fill="#1b5e20", fs=8.5, bold=True))

# UF skid
iso_p.append(iso_face([(0.10, 0.10, 0), (1.62, 0.10, 0), (1.62, 0.10, 1.62), (0.10, 0.10, 1.62)], "#ede7f6", "#5c35cc", 1.6, "6,2"))
iso_p.append(iso_face([(0.10, 0.10, 0), (1.62, 0.10, 0), (1.62, 1.45, 0), (0.10, 1.45, 0)], "#ddd5f8", "#5c35cc", 1.2, "5,2"))
iso_p.append(iso_face([(1.62, 0.10, 0), (1.62, 1.45, 0), (1.62, 1.45, 1.62), (1.62, 0.10, 1.62)], "#ccc0f0", "#5c35cc", 1.2, "5,2"))
iso_p.append(iso_txt(0.86, 0.77, 1.05, "UF PRE-TX", fill="#4527a0", fs=8.5, bold=True))
iso_p.append(iso_txt(0.86, 0.77, 0.78, "F-01  |  0.02 µm PVDF", fill="#512da8", fs=7.5))

# HP Pump P-02
p02_ix = 2.72
iso_p.append(iso_face([(p02_ix-0.22, 0.88, 0), (p02_ix+0.22, 0.88, 0), (p02_ix+0.22, 1.38, 0), (p02_ix-0.22, 1.38, 0)], "#ffebee", "#c62828", 2.2))
iso_p.append(iso_face([(p02_ix-0.22, 0.88, 0), (p02_ix+0.22, 0.88, 0), (p02_ix+0.22, 0.88, 0.58), (p02_ix-0.22, 0.88, 0.58)], "#ffcdd2", "#c62828", 2.2))
iso_p.append(iso_txt(p02_ix, 0.68, 0.72, "P-02  HP PUMP", fill="#c62828", fs=8.5, bold=True))
iso_p.append(iso_txt(p02_ix, 0.68, 0.53, "60 bar  |  5.5 kW  |  Grundfos MTRE", fill="#c62828", fs=7.5))

# PX device
px_ix = 3.32
iso_p.append(iso_face([(px_ix, 0.82, 0), (px_ix+0.88, 0.82, 0), (px_ix+0.88, 0.82, 0.78), (px_ix, 0.82, 0.78)], "#e3f2fd", "#0277bd", 1.6, "5,2"))
iso_p.append(iso_face([(px_ix, 0.82, 0), (px_ix+0.88, 0.82, 0), (px_ix+0.88, 1.72, 0), (px_ix, 1.72, 0)], "#bbdefb", "#0277bd", 1.2, "5,2"))
iso_p.append(iso_txt(px_ix+0.44, 1.27, 0.52, "PX E-01", fill="#01579b", fs=8.5, bold=True))
iso_p.append(iso_txt(px_ix+0.44, 1.27, 0.32, "η = 96%  |  ERI PX-70", fill="#0277bd", fs=7.5))

# RO Vessel V-01 (approximated as elongated box)
ro_iy = 1.02
ro_ir = 0.115
ro_ix1 = 4.5
ro_ix2 = 11.0
ro_iz = 0.68
iso_p.append(iso_face(
    [(ro_ix1, ro_iy-ro_ir, ro_iz-ro_ir), (ro_ix2, ro_iy-ro_ir, ro_iz-ro_ir),
     (ro_ix2, ro_iy-ro_ir, ro_iz+ro_ir), (ro_ix1, ro_iy-ro_ir, ro_iz+ro_ir)],
    "#bbdefb", "#1565c0", 2.2))
iso_p.append(iso_face(
    [(ro_ix1, ro_iy-ro_ir, ro_iz+ro_ir), (ro_ix2, ro_iy-ro_ir, ro_iz+ro_ir),
     (ro_ix2, ro_iy+ro_ir, ro_iz+ro_ir), (ro_ix1, ro_iy+ro_ir, ro_iz+ro_ir)],
    "#ddeeff", "#1565c0", 2.2))
# Element tick marks on top face
for i in range(1, 6):
    ev_x = ro_ix1 + i * (ro_ix2 - ro_ix1) / 6
    lp1 = iso(ev_x, ro_iy-ro_ir, ro_iz+ro_ir)
    lp2 = iso(ev_x, ro_iy+ro_ir, ro_iz+ro_ir)
    iso_p.append(f'<line x1="{lp1[0]:.1f}" y1="{lp1[1]:.1f}" x2="{lp2[0]:.1f}" y2="{lp2[1]:.1f}" stroke="#1565c0" stroke-width="0.9" opacity="0.6"/>')
iso_p.append(iso_txt((ro_ix1+ro_ix2)/2, ro_iy-ro_ir-0.14, ro_iz+ro_ir+0.14, "V-01 — RO PRESSURE VESSEL", fill="#0d47a1", fs=9.5, bold=True))
iso_p.append(iso_txt((ro_ix1+ro_ix2)/2, ro_iy-ro_ir-0.14, ro_iz+ro_ir-0.04, "6 × Filmtec SW30XHR-400i  |  223 m²  |  J = 20 LMH  |  NDP = 17.7 bar", fill="#1565c0", fs=8))

# Saddle supports
for ssx in [5.0, 7.75, 10.5]:
    iso_p.append(iso_face(
        [(ssx-0.12, ro_iy-0.18, 0), (ssx+0.12, ro_iy-0.18, 0),
         (ssx+0.12, ro_iy-0.18, ro_iz-ro_ir), (ssx-0.12, ro_iy-0.18, ro_iz-ro_ir)],
        "#607d8b", "#455a64", 1.0))

# Permeate tank T-01
t01_ix = 11.12
iso_p.append(iso_face([(t01_ix, 0.14, 0), (t01_ix+0.92, 0.14, 0), (t01_ix+0.92, 0.14, 1.65), (t01_ix, 0.14, 1.65)], "#e8f5e9", "#2e7d32", 1.6))
iso_p.append(iso_face([(t01_ix, 0.14, 0), (t01_ix+0.92, 0.14, 0), (t01_ix+0.92, 1.55, 0), (t01_ix, 1.55, 0)], "#c8e6c9", "#2e7d32", 1.2))
iso_p.append(iso_txt(t01_ix+0.46, 0.84, 1.00, "T-01  PERMEATE", fill="#1b5e20", fs=8.5, bold=True))
iso_p.append(iso_txt(t01_ix+0.46, 0.84, 0.78, "20,000 L/d  |  &lt;500 ppm", fill="#2e7d32", fs=7.5))

# Flow lines
# SW inlet
p_sw = iso(0, 1.22, 0.52)
iso_p.append(f'<line x1="{p_sw[0]-40:.1f}" y1="{p_sw[1]:.1f}" x2="{p_sw[0]:.1f}" y2="{p_sw[1]:.1f}" stroke="#1565c0" stroke-width="3.5" marker-end="url(#aC)"/>')
iso_p.append(f'<text x="{p_sw[0]-44:.1f}" y="{p_sw[1]-8:.1f}" text-anchor="end" font-family="Arial" font-size="8" fill="#1565c0">SW IN  44.4 m³/d</text>')
# SW → UF
iso_p.append(iso_line(0.12, 1.22, 0.52, 1.62, 1.22, 0.52, "#1565c0", 2.5))
# UF → HP pump
iso_p.append(iso_line(1.62, 1.22, 0.52, p02_ix, 1.22, 0.52, "#1565c0", 2.5))
# HP pump → RO (bold)
iso_p.append(iso_line(p02_ix+0.22, 1.22, ro_iz, ro_ix1, 1.22, ro_iz, "#1565c0", 5.5))
# Permeate out
p_perm_in = iso((ro_ix1+ro_ix2)/2, ro_iy-ro_ir, ro_iz+ro_ir)
p_perm_tk = iso(t01_ix, 0.84, 1.3)
iso_p.append(f'<line x1="{p_perm_in[0]:.1f}" y1="{p_perm_in[1]:.1f}" x2="{p_perm_in[0]:.1f}" y2="{p_perm_in[1]-26:.1f}" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#aG)"/>')
iso_p.append(f'<line x1="{p_perm_in[0]:.1f}" y1="{p_perm_in[1]-26:.1f}" x2="{p_perm_tk[0]:.1f}" y2="{p_perm_tk[1]:.1f}" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#aG)"/>')
# Brine out
p_brine_o = iso(ro_ix2, ro_iy, ro_iz)
iso_p.append(f'<line x1="{p_brine_o[0]:.1f}" y1="{p_brine_o[1]:.1f}" x2="{p_brine_o[0]+36:.1f}" y2="{p_brine_o[1]+18:.1f}" stroke="#bf5600" stroke-width="3" marker-end="url(#aO)"/>')
iso_p.append(f'<text x="{p_brine_o[0]+40:.1f}" y="{p_brine_o[1]+22:.1f}" font-family="Arial" font-size="8" fill="#bf5600">BRINE  24,400 L/d  63.6 g/L  → PX</text>')
# Electrical DC
p_pv_e = iso(3.2, 0.3, CH_I)
p_inv_e = iso(2.55, 1.05, 0.52)
iso_p.append(f'<line x1="{p_pv_e[0]:.1f}" y1="{p_pv_e[1]:.1f}" x2="{p_inv_e[0]:.1f}" y2="{p_inv_e[1]:.1f}" stroke="#e67e22" stroke-width="1.8" stroke-dasharray="7,3" marker-end="url(#aY)"/>')
iso_p.append(f'<text x="{(p_pv_e[0]+p_inv_e[0])/2+8:.1f}" y="{(p_pv_e[1]+p_inv_e[1])/2:.1f}" font-family="Arial" font-size="8" fill="#e67e22">DC  70 kWh/day</text>')

# 3-D dimension annotations
p_l1_d = iso(0, CW_I, 0)
p_l2_d = iso(CL_I, CW_I, 0)
iso_p.append(f'<line x1="{p_l1_d[0]:.1f}" y1="{p_l1_d[1]+6:.1f}" x2="{p_l2_d[0]:.1f}" y2="{p_l2_d[1]+6:.1f}" stroke="#333" stroke-width="0.9" marker-start="url(#dL)" marker-end="url(#dR)"/>')
p_lm_d = iso(CL_I/2, CW_I, 0)
iso_p.append(f'<text x="{p_lm_d[0]:.1f}" y="{p_lm_d[1]+18:.1f}" text-anchor="middle" font-family="Arial" font-size="9" fill="#333">12.19 m</text>')

p_h1_d = iso(0, 0, 0)
p_h2_d = iso(0, 0, CH_I)
iso_p.append(f'<line x1="{p_h1_d[0]-6:.1f}" y1="{p_h1_d[1]:.1f}" x2="{p_h2_d[0]-6:.1f}" y2="{p_h2_d[1]:.1f}" stroke="#333" stroke-width="0.9" marker-start="url(#dL)" marker-end="url(#dR)"/>')
iso_p.append(f'<text x="{p_h2_d[0]-20:.1f}" y="{(p_h1_d[1]+p_h2_d[1])/2:.1f}" text-anchor="end" font-family="Arial" font-size="9" fill="#333">2.59 m</text>')

p_w1_d = iso(CL_I, 0, 0)
p_w2_d = iso(CL_I, CW_I, 0)
iso_p.append(f'<line x1="{p_w1_d[0]+6:.1f}" y1="{p_w1_d[1]:.1f}" x2="{p_w2_d[0]+6:.1f}" y2="{p_w2_d[1]:.1f}" stroke="#333" stroke-width="0.9" marker-start="url(#dL)" marker-end="url(#dR)"/>')
iso_p.append(f'<text x="{p_w2_d[0]+20:.1f}" y="{(p_w1_d[1]+p_w2_d[1])/2:.1f}" font-family="Arial" font-size="9" fill="#333">2.44 m</text>')

# Axis labels
ax_o = iso(-0.4, -0.4, 0)
ax_x = iso(1.1, -0.4, 0)
ax_y = iso(-0.4, 1.1, 0)
ax_z = iso(-0.4, -0.4, 1.0)
iso_p.append(f'<line x1="{ax_o[0]:.1f}" y1="{ax_o[1]:.1f}" x2="{ax_x[0]:.1f}" y2="{ax_x[1]:.1f}" stroke="#c62828" stroke-width="1.8" marker-end="url(#aO)"/>')
iso_p.append(f'<line x1="{ax_o[0]:.1f}" y1="{ax_o[1]:.1f}" x2="{ax_y[0]:.1f}" y2="{ax_y[1]:.1f}" stroke="#2e7d32" stroke-width="1.8" marker-end="url(#aG)"/>')
iso_p.append(f'<line x1="{ax_o[0]:.1f}" y1="{ax_o[1]:.1f}" x2="{ax_z[0]:.1f}" y2="{ax_z[1]:.1f}" stroke="#1565c0" stroke-width="1.8" marker-end="url(#aC)"/>')
iso_p.append(f'<text x="{ax_x[0]+5:.1f}" y="{ax_x[1]+4:.1f}" font-family="Arial" font-size="8" fill="#c62828">L (12.19 m)</text>')
iso_p.append(f'<text x="{ax_y[0]-12:.1f}" y="{ax_y[1]+4:.1f}" text-anchor="end" font-family="Arial" font-size="8" fill="#2e7d32">W (2.44 m)</text>')
iso_p.append(f'<text x="{ax_z[0]-4:.1f}" y="{ax_z[1]:.1f}" text-anchor="end" font-family="Arial" font-size="8" fill="#1565c0">H (2.59 m)</text>')

# Legend
lg_iy = H - 44 - 72
iso_p.append(f'<rect x="14" y="{lg_iy:.1f}" width="460" height="64" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
iso_p.append(txt(234, lg_iy+13, "FLOW LEGEND", fs=9, bold=True, fill="#333"))
iso_p.append(f'<line x1="24" y1="{lg_iy+30:.1f}" x2="66" y2="{lg_iy+30:.1f}" stroke="#1565c0" stroke-width="4.5"/>')
iso_p.append(txt(72, lg_iy+34, "Feed / HP seawater", fs=8, fill="#333", anchor="start"))
iso_p.append(f'<line x1="24" y1="{lg_iy+50:.1f}" x2="66" y2="{lg_iy+50:.1f}" stroke="#2e7d32" stroke-width="3.5"/>')
iso_p.append(txt(72, lg_iy+54, "Permeate (product)", fs=8, fill="#333", anchor="start"))
iso_p.append(f'<line x1="230" y1="{lg_iy+30:.1f}" x2="272" y2="{lg_iy+30:.1f}" stroke="#bf5600" stroke-width="3.5"/>')
iso_p.append(txt(278, lg_iy+34, "Brine reject", fs=8, fill="#333", anchor="start"))
iso_p.append(f'<line x1="230" y1="{lg_iy+50:.1f}" x2="272" y2="{lg_iy+50:.1f}" stroke="#e67e22" stroke-width="1.8" stroke-dasharray="6,3"/>')
iso_p.append(txt(278, lg_iy+54, "Electrical DC (dashed)", fs=8, fill="#333", anchor="start"))

iso_p.append(f'<rect x="488" y="{lg_iy:.1f}" width="696" height="64" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
iso_p.append(txt(836, lg_iy+13, "KEY DESIGN NUMBERS", fs=9, bold=True, fill="#333"))
iso_p.append(txt(496, lg_iy+28, "Osmotic pressure: π = 28.4 bar  (van't Hoff, i = 1.90, 35 g/L NaCl, 25°C)  |  ΔP operating = 60 bar", fs=8, fill="#333", anchor="start"))
iso_p.append(txt(496, lg_iy+42, "CP = 1.49 (Graetz–Lévêque)  |  π_membrane = 42.3 bar  |  NDP = 17.7 bar  |  Flux J = 20 LMH", fs=8, fill="#333", anchor="start"))
iso_p.append(txt(496, lg_iy+56, "SEC = 3.5 kWh/m³ (PX η = 96%)  |  E_day = 70 kWh  |  LCoW ≈ $2.16/m³ (±40%)  |  LFP 87.5 kWh", fs=8, fill="#333", anchor="start"))

iso_p.append(title_block("ARCH-R2-CAD-004", "SOLAR SPRO SYSTEM — ISOMETRIC VIEW", "Scale NTS  |  40 ft ISO Container  |  Viewed from SE above", "NTS"))

with open("deliverables/02_cad_concept/04_isometric.svg", "w") as f:
    f.write(svg_wrap("".join(iso_p)))
print("04_isometric.svg OK")


# ════════════════════════════════════════════════════════════════════════════
# 5. P&ID — Piping and Instrumentation Diagram
# ════════════════════════════════════════════════════════════════════════════
pid = []
pid.append(txt(W/2, 26, "PROCESS &amp; INSTRUMENTATION DIAGRAM (P&amp;ID) — SOLAR SPRO  20,000 L/DAY", fs=13, bold=True, fill="#1a3a6b"))
pid.append(txt(W/2, 42, "Scale NTS  |  ISA 5.1 instrument symbology  |  Sheet 1 of 1  |  All process data at design conditions (25°C, 35 g/L NaCl)", fs=8.5, fill="#555"))

# ── POWER SECTION (top-left) ─────────────────────────────────────────────────
# PV Array
pid.append(f'<rect x="16" y="55" width="105" height="60" fill="#fff8e1" stroke="#f57f17" stroke-width="1.6" rx="3"/>')
pid.append(txt(68, 72, "PV ARRAY", fs=9, bold=True, fill="#e65100"))
pid.append(txt(68, 85, "14.8 kWp | 37 × 400 W", fs=7.5, fill="#e65100"))
pid.append(txt(68, 97, "72.9 m² | 15° tilt", fs=7.5, fill="#e67e22"))
pid.append(txt(68, 108, "η = 21% | MPPT ctrl", fs=7, fill="#e67e22"))

# LFP Battery
pid.append(f'<rect x="134" y="55" width="105" height="60" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.6" rx="3"/>')
pid.append(txt(186, 72, "LFP BATTERY", fs=9, bold=True, fill="#1b5e20"))
pid.append(txt(186, 85, "BAT-01: 87.5 kWh", fs=7.5, fill="#1b5e20"))
pid.append(txt(186, 97, "48 V | 80% DoD", fs=7.5, fill="#2e7d32"))
pid.append(txt(186, 108, "CATL 280 Ah | BMS", fs=7, fill="#2e7d32"))

# Inverter
pid.append(f'<rect x="252" y="55" width="100" height="60" fill="#f3e5f5" stroke="#6a1b9a" stroke-width="1.6" rx="3"/>')
pid.append(txt(302, 72, "INVERTER", fs=9, bold=True, fill="#4a148c"))
pid.append(txt(302, 85, "INV-01", fs=8, fill="#4a148c"))
pid.append(txt(302, 97, "Victron 48/8000", fs=7.5, fill="#6a1b9a"))
pid.append(txt(302, 108, "8 kW AC | MPPT 150V", fs=7, fill="#6a1b9a"))

# DC connections (dashed orange)
pid.append(f'<line x1="121" y1="85" x2="134" y2="85" stroke="#e67e22" stroke-width="1.6" stroke-dasharray="4,2" marker-end="url(#aY)"/>')
pid.append(f'<line x1="239" y1="85" x2="252" y2="85" stroke="#e67e22" stroke-width="1.6" stroke-dasharray="4,2" marker-end="url(#aY)"/>')
pid.append(f'<line x1="352" y1="85" x2="395" y2="85" stroke="#e67e22" stroke-width="1.6" stroke-dasharray="4,2"/>')
pid.append(f'<line x1="395" y1="85" x2="395" y2="248" stroke="#e67e22" stroke-width="1.6" stroke-dasharray="4,2" marker-end="url(#aY)"/>')
pid.append(f'<text x="379" y="172" text-anchor="middle" font-family="Arial" font-size="8" fill="#e67e22" transform="rotate(-90 379 172)">DC power  70 kWh/day</text>')

# ── SEAWATER SOURCE ────────────────────────────────────────────────────────────
pid.append(f'<rect x="16" y="210" width="78" height="72" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.6" rx="3"/>')
pid.append(txt(55, 228, "SEAWATER", fs=9, bold=True, fill="#0d47a1"))
pid.append(txt(55, 241, "SOURCE", fs=9, bold=True, fill="#0d47a1"))
pid.append(txt(55, 254, "44.4 m³/d", fs=8, fill="#1565c0"))
pid.append(txt(55, 266, "35 g/L NaCl", fs=8, fill="#1565c0"))
pid.append(txt(55, 277, "25°C | pH 8.1", fs=7.5, fill="#1565c0"))

# ── ANTISCALANT D-01 ─────────────────────────────────────────────────────────
pid.append(f'<rect x="115" y="172" width="64" height="50" fill="#fce4ec" stroke="#ad1457" stroke-width="1.1" stroke-dasharray="5,2" rx="3"/>')
pid.append(txt(147, 189, "ANTISCALANT", fs=8, bold=True, fill="#880e4f"))
pid.append(txt(147, 201, "D-01", fs=8, fill="#880e4f"))
pid.append(txt(147, 212, "&lt;5 ppm Genesys SW", fs=7, fill="#ad1457"))
pid.append(f'<line x1="147" y1="222" x2="147" y2="244" stroke="#ad1457" stroke-width="1.2" stroke-dasharray="3,2" marker-end="url(#aY)"/>')

# ── LP PUMP P-01 ──────────────────────────────────────────────────────────────
pid.append(f'<circle cx="210" cy="246" r="24" fill="#fff8e1" stroke="#f57f17" stroke-width="2.2"/>')
pid.append(f'<path d="M192,246 Q210,224 228,246 Q210,268 192,246" fill="#ffe082" stroke="#f57f17" stroke-width="1.8"/>')
pid.append(txt(210, 241, "P", fs=10, bold=True, fill="#e65100"))
pid.append(txt(210, 254, "P-01", fs=8.5, fill="#e65100"))
pid.append(txt(210, 282, "LP | 2.5 bar", fs=8, fill="#555"))
pid.append(txt(210, 294, "1.85 m³/h", fs=7.5, fill="#555"))
pid.append(inst(210, 305, "FI-01", 210, 270))

# ── UF SKID F-01 ─────────────────────────────────────────────────────────────
pid.append(f'<rect x="258" y="208" width="108" height="96" fill="#ede7f6" stroke="#5c35cc" stroke-width="1.8" rx="5"/>')
pid.append(txt(312, 228, "UF PRE-TX", fs=10, bold=True, fill="#4527a0"))
pid.append(txt(312, 242, "F-01", fs=9.5, fill="#512da8"))
pid.append(txt(312, 256, "Dow FilmTec UF", fs=8, fill="#5c35cc"))
pid.append(txt(312, 269, "SDI &lt;3 | 0.02 µm", fs=8, fill="#5c35cc"))
pid.append(txt(312, 281, "PVDF hollow fibre", fs=7.5, fill="#5c35cc"))
pid.append(txt(312, 293, "CIP: NaOH / citric", fs=7, fill="#5c35cc"))
pid.append(inst(272, 197, "PT-01", 272, 208))
pid.append(inst(330, 197, "AT-01", 330, 208))

# ── HP PUMP P-02 ─────────────────────────────────────────────────────────────
pid.append(f'<circle cx="420" cy="256" r="28" fill="#ffebee" stroke="#c62828" stroke-width="2.5"/>')
pid.append(f'<path d="M399,256 Q420,228 441,256 Q420,284 399,256" fill="#ffcdd2" stroke="#c62828" stroke-width="2.2"/>')
pid.append(txt(420, 250, "P", fs=11, bold=True, fill="#b71c1c"))
pid.append(txt(420, 264, "P-02", fs=9, fill="#c62828"))
pid.append(txt(420, 298, "HP PUMP", fs=9.5, bold=True, fill="#c62828"))
pid.append(txt(420, 312, "60 bar | 5.5 kW", fs=8.5, fill="#c62828"))
pid.append(txt(420, 325, "Grundfos MTRE 45-3", fs=8, fill="#c62828"))
pid.append(txt(420, 337, "VFD speed control", fs=7.5, fill="#c62828"))

# PSV
pid.append(f'<rect x="452" y="232" width="58" height="26" fill="#fff3e0" stroke="#e65100" stroke-width="1" rx="2"/>')
pid.append(txt(481, 243, "PSV-01", fs=8.5, bold=True, fill="#e65100"))
pid.append(txt(481, 254, "set 70 bar", fs=7.5, fill="#e65100"))
pid.append(f'<line x1="452" y1="245" x2="448" y2="245" stroke="#e65100" stroke-width="0.9" stroke-dasharray="3,2"/>')
pid.append(inst(420, 207, "PT-02", 420, 228))

# ── PX DEVICE E-01 ────────────────────────────────────────────────────────────
pid.append(f'<rect x="512" y="308" width="98" height="68" fill="#e3f2fd" stroke="#0277bd" stroke-width="1.6" stroke-dasharray="5,2" rx="5"/>')
pid.append(txt(561, 329, "PX DEVICE", fs=10, bold=True, fill="#01579b"))
pid.append(txt(561, 344, "E-01", fs=9.5, fill="#0277bd"))
pid.append(txt(561, 358, "ERI PX-70", fs=8.5, fill="#0277bd"))
pid.append(txt(561, 370, "η = 96% | isobaric", fs=8, fill="#0277bd"))

# ── RO PRESSURE VESSEL V-01 ───────────────────────────────────────────────────
# Expanded to use the full width of the 1200px canvas
pid.append(f'<rect x="630" y="208" width="530" height="130" fill="#e3f2fd" stroke="#1565c0" stroke-width="2.5" rx="8"/>')
for i in range(1, 6):
    x_div = 630 + i * 530 / 6
    pid.append(f'<line x1="{x_div:.1f}" y1="208" x2="{x_div:.1f}" y2="338" stroke="#1565c0" stroke-width="0.9" opacity="0.6"/>')
pid.append(txt(895, 228, "RO PRESSURE VESSEL — V-01", fs=11, bold=True, fill="#0d47a1"))
pid.append(txt(895, 244, "6 × Filmtec SW30XHR-400i  |  8\" × 40\"  (203 mm OD × 1016 mm per element)", fs=8.5, fill="#1565c0"))
pid.append(txt(895, 258, "Active membrane area: 6 × 37.2 = 223 m²  |  FRP vessel Codeline 80S-6, PN 80 bar", fs=8.5, fill="#1565c0"))
pid.append(txt(895, 272, "Feed: 44.4 m³/d @ 60 bar, 25°C  |  Recovery: 45%  |  Rejection: 99.75%  |  NaCl permeate &lt;500 ppm", fs=8, fill="#1565c0"))
pid.append(txt(895, 285, "Permeate: 20,000 L/d  |  Brine: 24,400 L/d @ 63.6 g/L  |  Flux J = 20 L/(m²·h)", fs=8, fill="#1565c0"))
pid.append(txt(895, 298, "CP factor: 1.49 (Graetz–Lévêque)  |  Effective osmotic pressure π_m = 42.3 bar  |  NDP = 17.7 bar", fs=8, fill="#1565c0"))
pid.append(txt(895, 311, "Chemical dosing: antiscalant &lt;5 ppm Genesys SW  |  pH adjust H₂SO₄ to pH 7.5", fs=7.5, fill="#555"))
pid.append(txt(895, 323, "Thermodynamic min: 0.72 kWh/m³  |  Actual SEC (with PX): 3.5 kWh/m³  |  η_th = 20.6%", fs=7.5, fill="#555"))

# Instruments along RO vessel
for (tag_i, xi_i) in [("PI-01", 650), ("PT-03", 698), ("AT-02", 778), ("FI-02", 870), ("PI-02", 980)]:
    pid.append(inst(xi_i, 196, tag_i, xi_i, 208))

# ── PERMEATE STORAGE T-01 ─────────────────────────────────────────────────────
pid.append(f'<rect x="1172" y="208" width="22" height="100" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.6" rx="3"/>')
pid.append(txt(1183, 248, "PERMEATE T-01", fs=7.5, bold=True, fill="#1b5e20", anchor="middle"))
# Rotated text
pid.append(f'<text x="1183" y="248" text-anchor="middle" font-family="Arial" font-size="8" font-weight="bold" fill="#1b5e20" transform="rotate(-90 1183 258)">PERMEATE T-01</text>')
pid.append(f'<text x="1183" y="290" text-anchor="middle" font-family="Arial" font-size="7.5" fill="#2e7d32" transform="rotate(-90 1183 290)">20,000 L/d  &lt;500 ppm</text>')
pid.append(inst(1183, 196, "LI-01", 1183, 208))

# ── BRINE DISPOSAL ────────────────────────────────────────────────────────────
pid.append(f'<rect x="1088" y="430" width="80" height="60" fill="#fff8e1" stroke="#e67e22" stroke-width="1.5" rx="3"/>')
pid.append(txt(1128, 451, "BRINE", fs=9.5, bold=True, fill="#e65100"))
pid.append(txt(1128, 465, "DISPOSAL", fs=8.5, fill="#e65100"))
pid.append(txt(1128, 478, "24,400 L/d", fs=8, fill="#e67e22"))
pid.append(txt(1128, 489, "63.6 g/L", fs=7.5, fill="#e67e22"))

# ── FLOW LINES ────────────────────────────────────────────────────────────────
# SW → P-01
pid.append(f'<line x1="94" y1="246" x2="186" y2="246" stroke="#1565c0" stroke-width="2.5" marker-end="url(#aC)"/>')
pid.append(txt(140, 240, "44.4 m³/d", fs=8, fill="#1565c0"))
# P-01 → UF
pid.append(f'<line x1="234" y1="246" x2="258" y2="246" stroke="#1565c0" stroke-width="2.5" marker-end="url(#aC)"/>')
# UF → P-02
pid.append(f'<line x1="366" y1="256" x2="392" y2="256" stroke="#1565c0" stroke-width="2.5" marker-end="url(#aC)"/>')
pid.append(txt(379, 250, "SDI &lt;3", fs=7.5, fill="#555"))
# P-02 → RO (HP double line)
pid.append(f'<line x1="448" y1="256" x2="630" y2="256" stroke="#1565c0" stroke-width="5.5" marker-end="url(#aC)"/>')
pid.append(f'<line x1="455" y1="249" x2="630" y2="249" stroke="#1565c0" stroke-width="1" opacity="0.3"/>')
pid.append(f'<rect x="492" y="241" width="76" height="14" fill="#c62828" rx="2"/>')
pid.append(txt(530, 251, "HP 60 bar →", fs=8, bold=True, fill="white"))
# Permeate: RO → T-01
pid.append(f'<line x1="1160" y1="252" x2="1172" y2="252" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#aG)"/>')
pid.append(txt(1155, 247, "20 kL/d", fs=7.5, fill="#1b5e20", anchor="end"))
# Brine: RO → down → PX → brine disposal
pid.append(f'<line x1="1160" y1="286" x2="1155" y2="286" stroke="#bf5600" stroke-width="2.2"/>')
pid.append(f'<line x1="1155" y1="286" x2="1155" y2="460" stroke="#bf5600" stroke-width="2.2"/>')
pid.append(f'<line x1="1155" y1="460" x2="1168" y2="460" stroke="#bf5600" stroke-width="2.2" marker-end="url(#aO)"/>')
pid.append(f'<text x="1160" y="390" text-anchor="start" font-family="Arial" font-size="8" fill="#bf5600" transform="rotate(-90 1160 390)">brine  24,400 L/d  63.6 g/L →</text>')
# Brine high-pressure side → PX
pid.append(f'<line x1="1148" y1="300" x2="1142" y2="300" stroke="#bf5600" stroke-width="1.8"/>')
pid.append(f'<line x1="1142" y1="300" x2="1142" y2="390" stroke="#bf5600" stroke-width="1.8"/>')
pid.append(f'<line x1="1142" y1="390" x2="610" y2="390" stroke="#bf5600" stroke-width="1.8" marker-end="url(#aO)"/>')
pid.append(txt(880, 385, "← brine high-pressure side → PX energy recovery (η = 96%)", fs=8, fill="#bf5600"))
# PX → HP pump suction (recovered pressure)
pid.append(f'<line x1="512" y1="352" x2="460" y2="352" stroke="#0277bd" stroke-width="2.2" stroke-dasharray="6,2" marker-end="url(#aC)"/>')
pid.append(f'<line x1="460" y1="352" x2="460" y2="284" stroke="#0277bd" stroke-width="2.2" stroke-dasharray="6,2" marker-end="url(#aC)"/>')
pid.append(txt(486, 370, "pre-pressurised SW → HP suction (PX outlet)", fs=7.5, fill="#0277bd"))

# ── LEGEND ────────────────────────────────────────────────────────────────────
lg_py = H - 44 - 75
pid.append(f'<rect x="14" y="{lg_py:.1f}" width="560" height="67" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
pid.append(txt(290, lg_py+13, "LINE &amp; INSTRUMENT LEGEND", fs=9, bold=True, fill="#333"))
pid.append(f'<line x1="24" y1="{lg_py+28:.1f}" x2="68" y2="{lg_py+28:.1f}" stroke="#1565c0" stroke-width="5"/>')
pid.append(txt(74, lg_py+33, "Feed / HP process line", fs=8.5, fill="#333", anchor="start"))
pid.append(f'<line x1="24" y1="{lg_py+46:.1f}" x2="68" y2="{lg_py+46:.1f}" stroke="#2e7d32" stroke-width="3.5"/>')
pid.append(txt(74, lg_py+51, "Permeate line", fs=8.5, fill="#333", anchor="start"))
pid.append(f'<line x1="24" y1="{lg_py+62:.1f}" x2="68" y2="{lg_py+62:.1f}" stroke="#bf5600" stroke-width="3.5"/>')
pid.append(txt(74, lg_py+67, "Brine reject line", fs=8.5, fill="#333", anchor="start"))
pid.append(f'<line x1="250" y1="{lg_py+28:.1f}" x2="294" y2="{lg_py+28:.1f}" stroke="#e67e22" stroke-width="2" stroke-dasharray="5,2"/>')
pid.append(txt(300, lg_py+33, "Electrical DC (dashed)", fs=8.5, fill="#333", anchor="start"))
pid.append(f'<line x1="250" y1="{lg_py+46:.1f}" x2="294" y2="{lg_py+46:.1f}" stroke="#0277bd" stroke-width="2" stroke-dasharray="6,2"/>')
pid.append(txt(300, lg_py+51, "PX → HP pump suction (pressurised)", fs=8.5, fill="#333", anchor="start"))
pid.append(f'<line x1="250" y1="{lg_py+62:.1f}" x2="294" y2="{lg_py+62:.1f}" stroke="#ad1457" stroke-width="1.5" stroke-dasharray="4,2"/>')
pid.append(txt(300, lg_py+67, "Chemical dosing (dashed)", fs=8.5, fill="#333", anchor="start"))

# Instrument key
pid.append(f'<rect x="588" y="{lg_py:.1f}" width="596" height="67" fill="#f5f5f5" stroke="#ccc" stroke-width="0.8" rx="2"/>')
pid.append(txt(886, lg_py+13, "INSTRUMENT TAG KEY", fs=9, bold=True, fill="#333"))
tags_key = [("PT", "Pressure Transmitter"), ("PI", "Pressure Indicator (local gauge)"),
            ("FI", "Flow Indicator"), ("AT", "Analyser Transmitter (conductivity/TDS)"), ("LI", "Level Indicator")]
for i_k, (t_k, d_k) in enumerate(tags_key):
    col_k = 598 + (i_k % 2) * 300
    row_k = lg_py + 28 + (i_k // 2) * 20
    pid.append(inst(col_k + 10, row_k - 4, t_k))
    pid.append(txt(col_k + 24, row_k, f"= {d_k}", fs=8, fill="#333", anchor="start"))

pid.append(title_block("ARCH-R2-CAD-005", "SOLAR SPRO SYSTEM — P&amp;ID (PROCESS &amp; INSTRUMENTATION DIAGRAM)", "Scale NTS  |  ISA 5.1  |  Sheet 1 of 1", "NTS"))

with open("deliverables/02_cad_concept/05_pid.svg", "w") as f:
    f.write(svg_wrap("".join(pid)))
print("05_pid.svg OK")

print("\nAll 5 SVG files generated successfully.")
