import {
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  investigationRepository,
} from "@/repositories";

import type {
  CreateInvestigationInput,
} from "@/repositories/InvestigationRepository";

import {
  InvestigationExecutionService,
} from "@/services/InvestigationExecutionService";

import type {
  Investigation,
} from "@/types/investigation";

import {
  InvestigationContext,
} from "./InvestigationContext";

type InvestigationProviderProps = {
  children: ReactNode;
};

export function InvestigationProvider({
  children,
}: InvestigationProviderProps) {
  const [, setVersion] = useState(0);

  const executionService = useMemo(
    () =>
      new InvestigationExecutionService(
        investigationRepository,
      ),
    [],
  );

  function refresh() {
    setVersion((version) => version + 1);
  }

  function getById(
    id: string,
  ): Investigation | undefined {
    return investigationRepository.getById(id);
  }

  function createAndStart(
    input: CreateInvestigationInput,
  ): Investigation | undefined {
    const investigation =
      investigationRepository.create(input);

    const started =
      executionService.start(investigation.id);

    refresh();

    return started;
  }

  function start(
    id: string,
  ): Investigation | undefined {
    const result =
      executionService.start(id);

    refresh();

    return result;
  }

  function setAnalyzing(
    id: string,
  ): Investigation | undefined {
    const result =
      executionService.setAnalyzing(id);

    refresh();

    return result;
  }

  function complete(
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
  ): Investigation | undefined {
    const result =
      executionService.complete(
        id,
        results,
      );

    refresh();

    return result;
  }

  function fail(
    id: string,
  ): Investigation | undefined {
    const result =
      executionService.fail(id);

    refresh();

    return result;
  }

  const value = {
    investigations:
      investigationRepository.list(),
    getById,
    createAndStart,
    start,
    setAnalyzing,
    complete,
    fail,
    refresh,
  };

  return (
    <InvestigationContext.Provider
      value={value}
    >
      {children}
    </InvestigationContext.Provider>
  );
}
