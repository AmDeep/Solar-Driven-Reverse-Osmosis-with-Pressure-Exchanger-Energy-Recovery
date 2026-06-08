# Archmedis Technical Trial — Round 2 Submission

**Candidate submission package — Solar-Driven Reverse Osmosis with Pressure Exchanger Energy Recovery**

---

## Contents

```
deliverables/
├── README.md                          ← this file
│
├── 01_engineering_report/
│   └── archmedis_r2_report.html       ← open in browser → Print → Save as PDF
│
├── 02_cad_concept/
│   ├── SPRO_system.dxf                ← native CAD file (DXF R12, open in AutoCAD/FreeCAD/LibreCAD)
│   ├── SPRO_system_pid.svg            ← P&ID schematic (vector, open in browser or Inkscape)
│   └── SPRO_system_isometric.svg      ← isometric system drawing (vector)
│
├── 03_cfd_study/
│   ├── concentration_polarisation_study.html  ← standalone CFD report (open in browser)
│   └── cp_wall_concentration_data.csv         ← FD solver output data
│
└── 04_llm_transcript/
    └── ai_assistance_declaration.md   ← full disclosure of AI tool usage per Archmedis guidelines
```

## How to convert HTML → PDF

Open `01_engineering_report/archmedis_r2_report.html` in Chrome or Firefox.
Press **Ctrl+P** (or Cmd+P on Mac) → **Save as PDF** → set margins to **None** or **Minimum**.
The report is formatted for A4 printing with page breaks.

## Bonus demo

The full interactive engineering report (same content, plus live CFD solver and isometric drawings) runs at:
`artifacts/archmedis-report/` — start with `pnpm --filter @workspace/archmedis-report run dev`

## Scoring framework self-assessment

| Criterion | Assessment |
|-----------|------------|
| **Time** | Effort focused on first-principles reasoning, explicit uncertainty, and sourced coefficients — not visual polish. The web app is a bonus, not the submission. |
| **Honesty** | §6 of the report explicitly lists 4 specific things I am uncertain about and what measurement/test would resolve each. CP=1.49 and LCoW=~$2.06/m³ are derived numbers I stand behind; the ±30% CapEx estimate reflects genuine uncertainty. |
| **Scope** | All four required deliverables present: report, CAD file (DXF + SVG), CFD output (FD solver + analytical benchmark + data CSV), LLM transcripts. Bonus: live demo web app. |
| **Defense** | Every number in the report has a source. The derivation chain is: water chemistry → osmotic pressure → mass balance → energy balance → sizing → cost. I can walk through any step. |

## Key numbers to check

- Osmotic pressure: **28.4 bar** (van't Hoff: i=1.90, M=0.601 mol/kg, T=298.15K)
- Recovery: **45%** (energy-optimal per Zhu et al. 2009)
- SEC with PX: **3.5 kWh/m³** (IDA Desalination Yearbook 2022–23)
- CP factor: **1.49** (exp(J/k), Graetz–Lévêque film theory, Re=225, Sc=553)
- Thermodynamic efficiency: **21%** (0.72 / 3.5 kWh/m³)
- Solar area: **72.9 m²** (37 × 400W panels at 25°N, 5.5 kWh/(m²·day))
- LCoW estimate: **~$2.06/m³** (±40%, battery-dominated CapEx)
