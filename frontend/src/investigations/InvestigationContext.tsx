import { createContext } from "react";

import type {
  CreateInvestigationInput,
} from "@/repositories/InvestigationRepository";

import type {
  Investigation,
} from "@/types/investigation";

export type InvestigationContextValue = {
  investigations: Investigation[];

  getById(
    id: string,
  ): Investigation | undefined;

  createAndStart(
    input: CreateInvestigationInput,
  ): Investigation | undefined;

  start(
    id: string,
  ): Investigation | undefined;

  setAnalyzing(
    id: string,
  ): Investigation | undefined;

  complete(
    id: string,
    results: Pick<
      Investigation,
      | "risk"
      | "riskScore"
      | "resources"
      | "findings"
      | "attackPaths"
      | "findingsList"
    >,
  ): Investigation | undefined;

  fail(
    id: string,
  ): Investigation | undefined;

  refresh(): void;
};

export const InvestigationContext =
  createContext<
    InvestigationContextValue | undefined
  >(undefined);
