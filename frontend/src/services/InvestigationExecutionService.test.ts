import { describe, expect, it } from "vitest";

import { investigations } from "@/data/investigations";
import { InMemoryInvestigationRepository } from "@/repositories/InMemoryInvestigationRepository";

import { InvestigationExecutionService } from "./InvestigationExecutionService";

function createService() {
  const repository =
    new InMemoryInvestigationRepository(
      investigations.map((investigation) => ({
        ...investigation,
        findingsList: [...investigation.findingsList],
      })),
    );

  const service =
    new InvestigationExecutionService(repository);

  return {
    repository,
    service,
  };
}

describe("InvestigationExecutionService", () => {
  it("moves a queued investigation to running", () => {
    const { repository, service } = createService();

    const investigation = repository.create({
      name: "Execution lifecycle test",
      provider: "AWS",
      environment: "Production",
      type: "Cloud Security",
    });

    expect(investigation.status).toBe("Queued");

    const result = service.start(investigation.id);

    expect(result?.status).toBe("Running");
  });

  it("moves a running investigation to analyzing", () => {
    const { repository, service } = createService();

    const investigation = repository.create({
      name: "Analysis lifecycle test",
      provider: "AWS",
      environment: "Production",
      type: "Cloud Security",
    });

    service.start(investigation.id);

    const result = service.setAnalyzing(
      investigation.id,
    );

    expect(result?.status).toBe("Analyzing");
  });

  it("completes an analyzing investigation with results", () => {
    const { repository, service } = createService();

    const investigation = repository.create({
      name: "Completion lifecycle test",
      provider: "AWS",
      environment: "Production",
      type: "Cloud Security",
    });

    service.start(investigation.id);
    service.setAnalyzing(investigation.id);

    const result = service.complete(
      investigation.id,
      {
        risk: "High",
        riskScore: 82,
        resources: 127,
        findings: 18,
        attackPaths: 6,
        findingsList: [
          {
            id: "finding-test",
            title: "Administrative IAM permission",
            severity: "High",
            resource: "production-admin-role",
          },
        ],
      },
    );

    expect(result?.status).toBe("Completed");
    expect(result?.risk).toBe("High");
    expect(result?.riskScore).toBe(82);
    expect(result?.resources).toBe(127);
    expect(result?.findings).toBe(18);
    expect(result?.attackPaths).toBe(6);
    expect(result?.findingsList).toHaveLength(1);
  });

  it("rejects skipping the running state", () => {
    const { repository, service } = createService();

    const investigation = repository.create({
      name: "Invalid transition test",
      provider: "AWS",
      environment: "Production",
      type: "Cloud Security",
    });

    const result = service.setAnalyzing(
      investigation.id,
    );

    expect(result?.status).toBe("Queued");
  });

  it("does not restart a completed investigation", () => {
    const { repository, service } = createService();

    const investigation = repository.create({
      name: "Completed restart test",
      provider: "AWS",
      environment: "Production",
      type: "Cloud Security",
    });

    repository.update(investigation.id, {
      status: "Completed",
    });

    const result = service.start(investigation.id);

    expect(result?.status).toBe("Completed");
  });

  it("moves an investigation to failed state", () => {
    const { repository, service } = createService();

    const investigation = repository.create({
      name: "Failure lifecycle test",
      provider: "AWS",
      environment: "Production",
      type: "Cloud Security",
    });

    const result = service.fail(
      investigation.id,
    );

    expect(result?.status).toBe("Failed");
  });

  it("returns undefined for an unknown investigation", () => {
    const { service } = createService();

    expect(
      service.start("inv-does-not-exist"),
    ).toBeUndefined();

    expect(
      service.setAnalyzing("inv-does-not-exist"),
    ).toBeUndefined();

    expect(
      service.fail("inv-does-not-exist"),
    ).toBeUndefined();
  });
});
