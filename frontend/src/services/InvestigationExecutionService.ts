import type { Investigation } from "@/types/investigation";
import type { InvestigationRepository } from "@/repositories/InvestigationRepository";

export class InvestigationExecutionService {
  private readonly repository: InvestigationRepository;

  constructor(repository: InvestigationRepository) {
    this.repository = repository;
  }

  start(
    investigationId: string,
  ): Investigation | undefined {
    const investigation =
      this.repository.getById(investigationId);

    if (!investigation) {
      return undefined;
    }

    if (
      investigation.status !== "Queued" &&
      investigation.status !== "Failed"
    ) {
      return investigation;
    }

    return this.repository.update(
      investigationId,
      {
        status: "Running",
        updated: "Just now",
      },
    );
  }

  setAnalyzing(
    investigationId: string,
  ): Investigation | undefined {
    const investigation =
      this.repository.getById(investigationId);

    if (!investigation) {
      return undefined;
    }

    if (investigation.status !== "Running") {
      return investigation;
    }

    return this.repository.update(
      investigationId,
      {
        status: "Analyzing",
        updated: "Just now",
      },
    );
  }

  complete(
    investigationId: string,
    results: Pick<
      Investigation,
      | "risk"
      | "riskScore"
      | "resources"
      | "findings"
      | "attackPaths"
      | "findingsList"
    >,
  ): Investigation | undefined {
    const investigation =
      this.repository.getById(investigationId);

    if (!investigation) {
      return undefined;
    }

    if (investigation.status !== "Analyzing") {
      return investigation;
    }

    return this.repository.update(
      investigationId,
      {
        ...results,
        status: "Completed",
        updated: "Just now",
      },
    );
  }

  fail(
    investigationId: string,
  ): Investigation | undefined {
    const investigation =
      this.repository.getById(investigationId);

    if (!investigation) {
      return undefined;
    }

    return this.repository.update(
      investigationId,
      {
        status: "Failed",
        updated: "Just now",
      },
    );
  }
}
