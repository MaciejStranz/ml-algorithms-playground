import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, test, vi } from "vitest";
import { http, HttpResponse } from "msw";

import { server } from "../testServer";
import ExperimentsList from "../../components/Experiments/ExperimentsList";

const EXPERIMENTS_LIST_URL = /\/api\/experiments\/$/;
const EXPERIMENT_DELETE_URL = /\/api\/experiments\/\d+\/$/;

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  });
}

function renderList() {
  const queryClient = createTestQueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/"]}>
        <ExperimentsList />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("ExperimentsList", () => {
  test("shows a loading state while experiments are being fetched", async () => {
    server.use(
      http.get(EXPERIMENTS_LIST_URL, async () => {
        await new Promise((resolve) => setTimeout(resolve, 150));
        return HttpResponse.json([], { status: 200 });
      })
    );

    renderList();

    expect(screen.getByText(/loading experiments/i)).toBeInTheDocument();
    expect(await screen.findByText(/no experiments yet/i)).toBeInTheDocument();
  });

  test("renders experiments using algorithm_variant contract", async () => {
    server.use(
      http.get(EXPERIMENTS_LIST_URL, () =>
        HttpResponse.json(
          [
            {
              id: 11,
              dataset: { id: 1, name: "Iris" },
              algorithm_variant: {
                id: 101,
                code: "svc",
                algorithm: {
                  id: 1,
                  code: "svm",
                  name: "Support Vector Machine",
                },
              },
              task: "multiclass_classification",
              created_at: "2025-12-06T03:08:18.950169Z",
              status: "finished",
              hyperparameters: { C: 1, kernel: "rbf" },
              metrics: { accuracy: 0.9333333333333333 },
            },
            {
              id: 7,
              dataset: { id: 5, name: "Sinusoid Function" },
              algorithm_variant: {
                id: 202,
                code: "rf_regressor",
                algorithm: {
                  id: 2,
                  code: "random_forest",
                  name: "Random Forest",
                },
              },
              task: "regression",
              created_at: "2025-12-06T02:09:41.798903Z",
              status: "finished",
              hyperparameters: {},
              metrics: { r2: 0.9985618258401496 },
            },
          ],
          { status: 200 }
        )
      )
    );

    renderList();

    expect(await screen.findByText(/experiment #11/i)).toBeInTheDocument();
    expect(screen.getByText(/support vector machine/i)).toBeInTheDocument();
    expect(screen.getByText(/iris/i)).toBeInTheDocument();
    expect(screen.getByText("svc")).toBeInTheDocument();

    expect(screen.getByText(/experiment #7/i)).toBeInTheDocument();
    expect(screen.getByText(/random forest/i)).toBeInTheDocument();
    expect(screen.getByText(/sinusoid function/i)).toBeInTheDocument();
    expect(screen.getByText("rf_regressor")).toBeInTheDocument();

    expect(screen.getByText(/93\.3%/)).toBeInTheDocument();
    expect(screen.getByText(/0\.9986/)).toBeInTheDocument();
  });

  test("shows an empty state when the user has no experiments", async () => {
    server.use(
      http.get(EXPERIMENTS_LIST_URL, () =>
        HttpResponse.json([], { status: 200 })
      )
    );

    renderList();

    expect(await screen.findByText(/no experiments yet/i)).toBeInTheDocument();
  });

  test("deletes an experiment after confirmation and removes it from the list", async () => {
    const user = userEvent.setup();

    let experiments = [
      {
        id: 11,
        dataset: { id: 1, name: "Iris" },
        algorithm_variant: {
          id: 101,
          code: "svc",
          algorithm: {
            id: 1,
            code: "svm",
            name: "Support Vector Machine",
          },
        },
        task: "multiclass_classification",
        created_at: "2025-12-06T03:08:18.950169Z",
        status: "finished",
        hyperparameters: {},
        metrics: { accuracy: 1.0 },
      },
      {
        id: 7,
        dataset: { id: 5, name: "Sinusoid Function" },
        algorithm_variant: {
          id: 202,
          code: "rf_regressor",
          algorithm: {
            id: 2,
            code: "random_forest",
            name: "Random Forest",
          },
        },
        task: "regression",
        created_at: "2025-12-06T02:09:41.798903Z",
        status: "finished",
        hyperparameters: {},
        metrics: { r2: 0.5 },
      },
    ];

    let deletedId = null;

    server.use(
      http.get(EXPERIMENTS_LIST_URL, () =>
        HttpResponse.json(experiments, { status: 200 })
      ),
      http.delete(EXPERIMENT_DELETE_URL, ({ request }) => {
        const url = new URL(request.url);
        const parts = url.pathname.split("/").filter(Boolean);
        deletedId = Number(parts[2]);

        experiments = experiments.filter((exp) => exp.id !== deletedId);

        return new HttpResponse(null, { status: 204 });
      })
    );

    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);

    renderList();

    expect(
      await screen.findByRole("link", { name: /experiment #11/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: /experiment #7/i })
    ).toBeInTheDocument();

    const deleteButtons = screen.getAllByRole("button", { name: /^delete$/i });
    await user.click(deleteButtons[0]);

    await waitFor(() => {
      expect(
        screen.queryByRole("link", { name: /experiment #11/i })
      ).not.toBeInTheDocument();
    });

    expect(screen.getByRole("link", { name: /experiment #7/i })).toBeInTheDocument();
    expect(deletedId).toBe(11);

    confirmSpy.mockRestore();
  });
});
