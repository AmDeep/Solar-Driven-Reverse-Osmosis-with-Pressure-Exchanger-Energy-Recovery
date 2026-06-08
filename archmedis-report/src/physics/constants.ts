// ============================================================
// SEAWATER THERMODYNAMIC CONSTANTS (sourced from literature)
// ============================================================
// Millero, F.J. (2010) Chemical Oceanography, CRC Press
// IDA Desalination Yearbook 2022-23

export const PHYSICS = {
  // Seawater composition
  SALINITY_G_PER_L: 35,         // g/L (Millero 2010, global avg)
  SALINITY_MOLAL: 0.601,        // mol/kg NaCl equivalent
  VANT_HOFF_FACTOR: 1.9,        // i for NaCl at 0.6 M (Pitzer model, Robinson & Stokes 1959)

  // Universal constants
  R: 8.314,                     // J/(mol·K) — universal gas constant
  T_K: 298.15,                  // K — 25°C operating temperature
  RHO_SEAWATER: 1025,           // kg/m³ — seawater density at 25°C, 35 ppt
  RHO_FRESHWATER: 997,          // kg/m³

  // Osmotic pressure (van't Hoff: π = iMRT)
  // π = 1.9 × 0.601 × 8.314 × 298.15 / 1000 = 2.837 MPa
  OSMOTIC_PRESSURE_MPA: 2.837,  // MPa = 28.37 bar

  // RO operating parameters (Filmtec SW30XHR-400 datasheet, DowDuPont)
  RO_OPERATING_PRESSURE_BAR: 60,   // bar — typical SWRO operating pressure
  RO_RECOVERY_RATIO: 0.45,         // 45% recovery (energy-efficiency optimum)
  RO_FLUX_LMH: 20,                 // L/(m²·h) — membrane flux at 60 bar
  RO_REJECTION: 0.9975,            // 99.75% NaCl rejection
  RO_MEMBRANE_AREA_PER_ELEMENT: 37.2, // m² — SW30XHR-400i element
  ELEMENTS_PER_VESSEL: 6,

  // Energy (Membrane Technology and Research, Baker 2012)
  SPECIFIC_ENERGY_WITH_PX_KWH_M3: 3.5,   // kWh/m³ with PX energy recovery
  SPECIFIC_ENERGY_NO_PX_KWH_M3: 7.2,     // kWh/m³ without energy recovery
  MIN_THERMODYNAMIC_WORK_KWH_M3: 0.72,   // Ideal (Carnot) minimum at 45% recovery
  PX_EFFICIENCY: 0.96,                   // Pressure exchanger isobaric efficiency

  // Solar (NREL PVWATTS, coastal Mediterranean / Red Sea)
  SOLAR_IRRADIANCE_KWH_M2_DAY: 5.5,   // kWh/(m²·day) peak sun hours
  PV_EFFICIENCY: 0.21,                 // Monocrystalline Si, STC (IEA PVPS 2023)
  SYSTEM_LOSSES: 0.83,                 // Inverter + cable + soiling losses

  // Mass transfer / CFD (diffusion of NaCl in water at 25°C)
  D_NACL_M2_S: 1.61e-9,    // m²/s — NaCl diffusivity, 25°C (CRC Handbook)
  NU_WATER: 8.9e-7,         // m²/s — kinematic viscosity of water at 25°C
  CHANNEL_HEIGHT_M: 0.001,  // m — feed spacer channel height (1 mm)
  CHANNEL_LENGTH_M: 0.85,   // m — SW30XHR element length
  FEED_VELOCITY_M_S: 0.1,   // m/s — typical crossflow velocity

  // Design target
  TARGET_OUTPUT_L_DAY: 20000,  // L/day
  TARGET_OUTPUT_M3_DAY: 20,    // m³/day
} as const;

// Derived calculations
export function calcOsmoticPressure(molality: number, i: number, T: number): number {
  return (i * molality * PHYSICS.R * T) / 1000; // MPa
}

export function calcSeawaterIntake(output_m3_day: number, recovery: number): number {
  return output_m3_day / recovery;
}

export function calcBrineOutput(intake: number, freshwater: number): number {
  return intake - freshwater;
}

export function calcEnergyRequired(output_m3_day: number, specific_energy: number): number {
  return output_m3_day * specific_energy; // kWh/day
}

export function calcSolarPanelArea(energy_kwh_day: number): number {
  const elec_per_m2 = PHYSICS.SOLAR_IRRADIANCE_KWH_M2_DAY * PHYSICS.PV_EFFICIENCY * PHYSICS.SYSTEM_LOSSES;
  return energy_kwh_day / elec_per_m2;
}

// CFD: Concentration polarization via film theory
// Sh = 1.85 (Re·Sc·d_h/L)^(1/3)  — Lévêque (Graetz–Nusselt analogy)
export function calcReynoldsNumber(U: number, d_h: number, nu: number): number {
  return (U * d_h) / nu;
}

export function calcSchmidtNumber(nu: number, D: number): number {
  return nu / D;
}

export function calcSherwoodNumber(Re: number, Sc: number, d_h: number, L: number): number {
  return 1.85 * Math.pow((Re * Sc * d_h) / L, 1 / 3);
}

export function calcMassTransferCoeff(Sh: number, D: number, d_h: number): number {
  return (Sh * D) / d_h; // m/s
}

export function calcConcentrationPolarization(J_m_s: number, k: number): number {
  return Math.exp(J_m_s / k); // CP = C_m / C_b
}

// Brine concentration profile along membrane element
export function calcBrineConcentration(
  C_feed: number,
  recovery_local: number,
  rejection: number
): number {
  return C_feed * (1 - (1 - rejection) * recovery_local) / (1 - recovery_local);
}
