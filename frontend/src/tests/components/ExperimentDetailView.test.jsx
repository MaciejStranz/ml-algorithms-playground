import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Routes, Route, useParams } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, test, vi } from "vitest";
import { http, HttpResponse } from "msw";

import { server } from "../testServer";
import ExperimentDetailView from "../../components/Experiments/ExperimentDetailView";

const EXPERIMENT_DETAIL_URL = /\/api\/experiments\/\d+\/$/;

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

function DetailRouteWrapper() {
  const { id } = useParams();
  return <ExperimentDetailView experimentId={id} />;
}

function renderApp(initialEntry) {
  const queryClient = createTestQueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[initialEntry]}>
        <Routes>
          <Route path="/" element={<div>HOME</div>} />
          <Route path="/experiments/:id" element={<DetailRouteWrapper />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("ExperimentDetailView", () => {
  test("renders experiment details and shows Accuracy (%) for classification", async () => {
    server.use(
      http.get(EXPERIMENT_DETAIL_URL, () =>
        HttpResponse.json(
          {
            id: 11,
            dataset: { id: 1, name: "Iris" },
            algorithm_variant: {
              id: 101,
              code: "svc",
              supported_tasks: ["multiclass_classification"],
              hyperparameter_specs: [],
              algorithm: {
                id: 1,
                code: "svm",
                name: "Support Vector Machine",
                kind: "classical",
                description: "SVM model",
              },
            },
            task: "multiclass_classification",
            created_at: "2025-12-06T03:08:18.950169Z",
            status: "finished",
            hyperparameters: { C: 1, kernel: "rbf" },
            test_size: 0.3,
            random_state: 42,
            include_predictions: true,
            include_probabilities: false,
            metrics: { accuracy: 0.9333333333333333 },
            predictions: null,
          },
          { status: 200 }
        )
      )
    );

    renderApp("/experiments/11");

    expect(
      await screen.findByRole("heading", { name: /experiment #11/i })
    ).toBeInTheDocument();

    expect(screen.getByText("finished")).toBeInTheDocument();
    expect(screen.getByText("multiclass_classification")).toBeInTheDocument();
    expect(screen.getByText("Iris")).toBeInTheDocument();
    expect(screen.getByText("Support Vector Machine")).toBeInTheDocument();
    expect(screen.getByText("svc")).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: /summary/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: /hyperparameters/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: /metrics/i })
    ).toBeInTheDocument();

    expect(screen.getByText("Accuracy")).toBeInTheDocument();
    expect(screen.getByText("93.3%")).toBeInTheDocument();

    expect(screen.getByText(/"kernel": "rbf"/i)).toBeInTheDocument();
    expect(screen.getByText(/"C": 1/i)).toBeInTheDocument();

    expect(screen.getByText(/"accuracy": 0\.933333/i)).toBeInTheDocument();
  });

  test("renders experiment details and shows R² for regression", async () => {
    server.use(
      http.get(EXPERIMENT_DETAIL_URL, () =>
        HttpResponse.json(
          {
            id: 7,
            dataset: { id: 5, name: "Sinusoid Function" },
            algorithm_variant: {
              id: 202,
              code: "rf_regressor",
              supported_tasks: ["regression"],
              hyperparameter_specs: [],
              algorithm: {
                id: 2,
                code: "random_forest",
                name: "Random Forest",
                kind: "classical",
                description: "Random Forest model",
              },
            },
            task: "regression",
            created_at: "2025-12-06T02:09:41.798903Z",
            status: "finished",
            hyperparameters: {},
            test_size: 0.3,
            random_state: 42,
            include_predictions: false,
            include_probabilities: false,
            metrics: { r2: 0.9985618258401496 },
            predictions: null,
          },
          { status: 200 }
        )
      )
    );

    renderApp("/experiments/7");

    expect(
      await screen.findByRole("heading", { name: /experiment #7/i })
    ).toBeInTheDocument();

    expect(screen.getByText("rf_regressor")).toBeInTheDocument();
    expect(screen.getByText("0.9986")).toBeInTheDocument();
  });

  test("deletes experiment after confirmation and redirects to home", async () => {
    const user = userEvent.setup();

    server.use(
      http.get(EXPERIMENT_DETAIL_URL, () =>
        HttpResponse.json(
          {
            id: 11,
            dataset: { id: 1, name: "Iris" },
            algorithm_variant: {
              id: 101,
              code: "svc",
              supported_tasks: ["multiclass_classification"],
              hyperparameter_specs: [],
              algorithm: {
                id: 1,
                code: "svm",
                name: "Support Vector Machine",
                kind: "classical",
                description: "SVM model",
              },
            },
            task: "multiclass_classification",
            created_at: "2025-12-06T03:08:18.950169Z",
            status: "finished",
            hyperparameters: {},
            test_size: 0.3,
            random_state: 42,
            include_predictions: false,
            include_probabilities: false,
            metrics: { accuracy: 1.0 },
            predictions: null,
          },
          { status: 200 }
        )
      )
    );

    let deletedId = null;

    server.use(
      http.delete(EXPERIMENT_DETAIL_URL, ({ request }) => {
        const url = new URL(request.url);
        const parts = url.pathname.split("/").filter(Boolean);
        deletedId = Number(parts[2]);
        return new HttpResponse(null, { status: 204 });
      })
    );

    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);

    renderApp("/experiments/11");

    expect(
      await screen.findByRole("heading", { name: /experiment #11/i })
    ).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /delete/i }));

    expect(await screen.findByText("HOME")).toBeInTheDocument();
    expect(deletedId).toBe(11);

    confirmSpy.mockRestore();
  });

  test("shows error state when experiment cannot be loaded", async () => {
    server.use(
      http.get(EXPERIMENT_DETAIL_URL, () =>
        HttpResponse.json({ detail: "Not found." }, { status: 404 })
      )
    );

    renderApp("/experiments/999");

    expect(await screen.findByText(/not found/i)).toBeInTheDocument();

    const back = screen.getByRole("link", { name: /back to home/i });
    expect(back).toHaveAttribute("href", "/");
  });
});
