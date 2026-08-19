import {
  investigations,
} from "@/data/investigations";

import type {
  Investigation,
} from "@/types/investigation";

import type {
  CreateInvestigationInput,
} from "./InvestigationRepository";

import type {
  LocalInvestigationRepository,
} from "./LocalInvestigationRepository";

function generateInvestigationId(): string {
  return `inv-${crypto.randomUUID()}`;
}

function createTimestamp(): string {
  return "Just now";
}

export class InMemoryInvestigationRepository
  implements LocalInvestigationRepository
{
  private readonly records: Investigation[];

  constructor(
    initialRecords: Investigation[] = investigations,
  ) {
    this.records = [...initialRecords];
  }

  create(
    input: CreateInvestigationInput,
  ): Investigation {
    const investigation: Investigation = {
      id: generateInvestigationId(),
      name: input.name,
      provider: input.provider,
      environment: input.environment,
      type: input.type,

      status: "Queued",
      risk: "Medium",
      riskScore: 0,

      resources: 0,
      findings: 0,
      attackPaths: 0,

      updated: createTimestamp(),

      findingsList: [],
      attackPathAnalysis: null,
      blastRadiusAnalysis: null,
      riskAssessment: null,
      reasoning: null,
      remediations: [],
    };

    this.records.unshift(investigation);

    return investigation;
  }

  getById(
    id: string,
  ): Investigation | undefined {
    return this.records.find(
      (investigation) =>
        investigation.id === id,
    );
  }

  update(
    id: string,
    patch: Partial<Omit<Investigation, "id">>,
  ): Investigation | undefined {
    const index = this.records.findIndex(
      (investigation) => investigation.id === id,
    );

    if (index === -1) {
      return undefined;
    }

    const current = this.records[index];

    if (!current) {
      return undefined;
    }

    const updated: Investigation = {
      ...current,
      ...patch,
    };

    this.records[index] = updated;

    return updated;
  }

  list(): Investigation[] {
    return [...this.records];
  }
}
