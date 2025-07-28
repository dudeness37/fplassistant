"use client";
import React, { createContext, useContext, useState } from "react";

type Risk = "low" | "medium" | "high";
type KpiTier = "100k" | "50k" | "10k";

type WizardState = {
  risk?: Risk;
  kpi?: KpiTier;
  setRisk: (r: Risk) => void;
  setKpi: (k: KpiTier) => void;
};

const Ctx = createContext<WizardState | undefined>(undefined);

export function WizardProvider({ children }: { children: React.ReactNode }) {
  const [risk, setRisk] = useState<Risk>();
  const [kpi, setKpi] = useState<KpiTier>("100k");
  return <Ctx.Provider value={{ risk, setRisk, kpi, setKpi }}>{children}</Ctx.Provider>;
}

export function useWizard() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useWizard must be used within WizardProvider");
  return ctx;
}
