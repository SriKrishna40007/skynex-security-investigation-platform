import type {
  CreateInvestigationInput,
} from "./InvestigationRepository";

import type {
  Investigation,
} from "@/types/investigation";

export interface LocalInvestigationRepository {
  create(
    input: CreateInvestigationInput,
  ): Investigation;

  getById(
    id: string,
  ): Investigation | undefined;

  update(
    id: string,
    patch: Partial<Omit<Investigation, "id">>,
  ): Investigation | undefined;

  list(): Investigation[];
}
