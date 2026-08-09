import { createContext } from "react";

import type {
  CreateInvestigationInput,
} from "@/repositories/InvestigationRepository";

import type {
  Investigation,
} from "@/types/investigation";

export type InvestigationContextValue = {
  investigations: Investigation[];

  isLoading: boolean;

  getById(
    id: string,
  ): Promise<Investigation | undefined>;

  createAndStart(
    input: CreateInvestigationInput,
  ): Promise<Investigation>;

  deleteInvestigation(
    id: string,
  ): Promise<void>;

  refresh(): Promise<void>;
};

export const InvestigationContext =
  createContext<
    InvestigationContextValue | undefined
  >(undefined);
