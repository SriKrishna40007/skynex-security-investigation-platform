import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  ApiInvestigationRepository,
} from "@/repositories/ApiInvestigationRepository";

import type {
  CreateInvestigationInput,
} from "@/repositories/InvestigationRepository";

import type {
  Investigation,
} from "@/types/investigation";

import {
  useAuth,
} from "@/auth/useAuth";

import {
  InvestigationContext,
} from "./InvestigationContext";

type InvestigationProviderProps = {
  children: ReactNode;
};

export function InvestigationProvider({
  children,
}: InvestigationProviderProps) {
  const { state: authState } = useAuth();

  const accessToken =
    authState.session?.accessToken;

  const repository = useMemo(
    () =>
      accessToken
        ? new ApiInvestigationRepository(
            accessToken,
          )
        : null,
    [accessToken],
  );

  const [investigations, setInvestigations] =
    useState<Investigation[]>([]);

  const [isLoading, setIsLoading] =
    useState(false);

  const refresh = useCallback(
    async () => {
      if (!repository) {
        setInvestigations([]);
        return;
      }

      setIsLoading(true);

      try {
        const records =
          await repository.list();

        setInvestigations(records);
      } finally {
        setIsLoading(false);
      }
    },
    [repository],
  );

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const getById = useCallback(
    async (
      id: string,
    ): Promise<
      Investigation | undefined
    > => {
      if (!repository) {
        return undefined;
      }

      return repository.getById(id);
    },
    [repository],
  );

  const createAndStart = useCallback(
    async (
      input: CreateInvestigationInput,
    ): Promise<Investigation> => {
      if (!repository) {
        throw new Error(
          "Authentication required.",
        );
      }

      const investigation =
        await repository.create(input);

      await refresh();

      return investigation;
    },
    [repository, refresh],
  );

  const deleteInvestigation = useCallback(
    async (id: string): Promise<void> => {
      if (!repository) {
        throw new Error(
          "Authentication required.",
        );
      }

      await repository.delete(id);

      await refresh();
    },
    [repository, refresh],
  );

  const value = useMemo(
    () => ({
      investigations,
      isLoading,
      getById,
      createAndStart,
      deleteInvestigation,
      refresh,
    }),
    [
      investigations,
      isLoading,
      getById,
      createAndStart,
      deleteInvestigation,
      refresh,
    ],
  );

  return (
    <InvestigationContext.Provider
      value={value}
    >
      {children}
    </InvestigationContext.Provider>
  );
}
