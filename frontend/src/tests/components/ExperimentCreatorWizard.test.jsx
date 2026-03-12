import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, test, vi, beforeEach } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "../testServer";

import ExperimentCreatorWizard from "../../components/ExperimentCreator/ExperimentCreatorWizard";

const DATASETS_URL = /\/api\/datasets\/$/;
const ALGORITHM_VARIANTS_URL = /\/api\/algorithm-variants\/(\?.*)?$/;
const EXPERIMENTS_CREATE_URL = /\/api\/experiments\/$/;

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

function renderApp() {
  const queryClient = createTestQueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/run"]}>
        <Routes>
          <Route path="/" element={<div>HOME</div>} />
          <Route path="/run" element={<ExperimentCreatorWizard />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
}

beforeEach(() => {
  localStorage.clear();
});

describe("ExperimentCreatorWizard", () => {
  test("happy path: select dataset + algorithm variant and run experiment -> POST + redirect to home", async () => {
    const user = userEvent.setup();

    let requestedTask = null;

    server.use(
      http.options(DATASETS_URL, () => new HttpResponse(null, { status: 204 })),
      http.options(ALGORITHM_VARIANTS_URL, () => new HttpResponse(null, { status: 204 })),
      http.options(EXPERIMENTS_CREATE_URL, () => new HttpResponse(null, { status: 204 })),

      http.get(DATASETS_URL, () =>
        HttpResponse.json(
          [
            {
              id: 1,
              code: "iris",
              name: "Iris",
              task: "multiclass_classification",
              n_samples: 150,
              n_features: 4,
              n_classes: 3,
              class_labels: ["0", "1", "2"],
              feature_names: ["f1", "f2", "f3", "f4"],
              target_name: "class",
            },
          ],
          { status: 200 }
        )
      ),

      http.get(ALGORITHM_VARIANTS_URL, ({ request }) => {
        const url = new URL(request.url);
        requestedTask = url.searchParams.get("task");

        return HttpResponse.json(
          [
            {
              id: 101,
              code: "svc",
              supported_tasks: ["binary_classification", "multiclass_classification"],
              hyperparameter_specs: [
                {
                  name: "C",
                  display_name: "C",
                  type: "float",
                  default: 1,
                  description: "Regularization.",
                  min: 0.0001,
                  max: 10000,
                  choices: null,
                  advanced: false,
                },
                {
                  name: "kernel",
                  display_name: "Kernel",
                  type: "choice",
                  default: "rbf",
                  description: "Kernel.",
                  min: null,
                  max: null,
                  choices: ["linear", "rbf"],
                  advanced: false,
                },
              ],
              algorithm: {
                id: 1,
                code: "svm",
                name: "Support Vector Machine",
                kind: "classical",
              },
            },
          ],
          { status: 200 }
        );
      })
    );

    let receivedPayload = null;

    server.use(
      http.post(EXPERIMENTS_CREATE_URL, async ({ request }) => {
        receivedPayload = await request.json();
        return HttpResponse.json({ id: 123 }, { status: 201 });
      })
    );

    const scrollSpy = vi.spyOn(window, "scrollTo").mockImplementation(() => {});

    renderApp();

    const irisHeading = await screen.findByRole("heading", { name: "Iris" });
    expect(irisHeading).toBeInTheDocument();

    await user.click(irisHeading);

    expect(await screen.findByText(/support vector machine/i)).toBeInTheDocument();

    await user.click(screen.getByText(/support vector machine/i));

    const runBtn = await screen.findByRole("button", { name: /run experiment/i });
    expect(runBtn).toBeEnabled();

    await user.click(runBtn);

    await waitFor(() => {
      expect(receivedPayload).not.toBeNull();
    });

    expect(requestedTask).toBe("multiclass_classification");

    expect(receivedPayload.dataset).toBe(1);
    expect(receivedPayload.algorithm_variant).toBe(101);
    expect(receivedPayload.algorithm).toBeUndefined();

    expect(receivedPayload.test_size).toBe(0.3);
    expect(receivedPayload.random_state).toBe(42);
    expect(receivedPayload.include_predictions).toBe(true);
    expect(receivedPayload.include_probabilities).toBe(false);

    expect(receivedPayload.hyperparameters).toMatchObject({
      C: 1,
      kernel: "rbf",
    });

    expect(await screen.findByText("HOME")).toBeInTheDocument();

    scrollSpy.mockRestore();
  });
});
