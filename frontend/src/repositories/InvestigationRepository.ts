import type {
  CloudProvider,
  Investigation,
  InvestigationEnvironment,
  InvestigationType,
} from "@/types/investigation";

export type CreateInvestigationInput = {
  name: string;
  provider: CloudProvider;
  environment: InvestigationEnvironment;
  type: InvestigationType;
};

export interface InvestigationRepository {
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
