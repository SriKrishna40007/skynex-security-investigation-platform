import type {
  Investigation,
} from "@/types/investigation";

export type CreateInvestigationInput = {
  name: string;
  provider: Investigation["provider"];
  environment: Investigation["environment"];
  type: Investigation["type"];

  terraformFile?: File;
  source?: string;
  target?: string;
};

export interface InvestigationRepository {
  create(
    input: CreateInvestigationInput,
  ): Promise<Investigation>;

  getById(
    id: string,
  ): Promise<Investigation | undefined>;

  delete(
    id: string,
  ): Promise<void>;

  list(): Promise<Investigation[]>;
}
