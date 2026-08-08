import { useContext } from "react";

import {
  InvestigationContext,
} from "./InvestigationContext";

export function useInvestigations() {
  const context =
    useContext(InvestigationContext);

  if (!context) {
    throw new Error(
      "useInvestigations must be used within InvestigationProvider.",
    );
  }

  return context;
}
