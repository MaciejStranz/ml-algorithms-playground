import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { http, HttpResponse } from "msw";
import { server } from "../testServer";

// Adjust path:
import ExperimentCreatorWizard from "../../components/ExperimentCreator/ExperimentCreatorWizard";

const DATASETS_URL = /\/api\/datasets\/$/;
const ALGORITHMS_URL = /\/api\/algorithms\/$/;
const EXPERIMENTS_CREATE_URL = /\/api\/experiments\/$/;

function renderApp() {
  render(
    <MemoryRouter initialEntries={["/run"]}>
      <Routes>
        <Route path="/" element={<div>HOME</div>} />
        <Route path="/run" element={<ExperimentCreatorWizard />} />
      </Routes>
    </MemoryRouter>
  );
}

describe("ExperimentCreatorWizard", () => {
  test("happy path: select dataset + algorithm and run experiment -> POST + redirect to home", async () => {
    const user = userEvent.setup();

    // --- Arrange: mock datasets + algorithms ---
    server.use(
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
      http.get(ALGORITHMS_URL, () =>
        HttpResponse.json(
          [
            {
              id: 1,
              code: "svm",
              name: "Support Vector Machine",
              kind: "classical",
              description: "SVM classifier/regressor.",
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
                  applicable_tasks: ["binary_classification", "multiclass_classification", "regression"],
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
                  applicable_tasks: ["binary_classification", "multiclass_classification", "regression"],
                  advanced: false,
                },
              ],
            },
          ],
          { status: 200 }
        )
      )
    );

    // Capture payload to assert correctness
    let receivedPayload = null;

    server.use(
      http.post(EXPERIMENTS_CREATE_URL, async ({ request }) => {
        receivedPayload = await request.json();
        return HttpResponse.json({ id: 123 }, { status: 201 });
      })
    );

    // Avoid jsdom error for window.scrollTo
    const scrollSpy = vi.spyOn(window, "scrollTo").mockImplementation(() => {});

    renderApp();

    // --- Wait for datasets to load ---
    const irisHeading = await screen.findByRole("heading", { name: "Iris" });
    expect(irisHeading).toBeInTheDocument();
    
    // --- Act: pick dataset ---
    // This assumes DatasetPicker renders something clickable with text "Iris".
    // If it doesn't, see note below about aria-labels.
    await user.click(irisHeading);

    // --- Algorithms section should appear (filtered by task) ---
    expect(await screen.findByText(/support vector machine/i)).toBeInTheDocument();

    // --- Act: pick algorithm ---
    await user.click(screen.getByText(/support vector machine/i));

    // Run button should appear now (hyperparams + config section are rendered)
    const runBtn = await screen.findByRole("button", { name: /run experiment/i });
    expect(runBtn).toBeEnabled();

    // --- Act: run ---
    await user.click(runBtn);

    // --- Assert: POST payload is correct ---
    await waitFor(() => {
      expect(receivedPayload).not.toBeNull();
    });

    expect(receivedPayload.dataset).toBe(1);
    expect(receivedPayload.algorithm).toBe(1);

    // Defaults from wizard state
    expect(receivedPayload.test_size).toBe(0.3);
    expect(receivedPayload.random_state).toBe(42);
    expect(receivedPayload.include_predictions).toBe(true);

    // Classification -> include_probabilities is false by default (and you reset it)
    expect(receivedPayload.include_probabilities).toBe(false);

    // Hyperparameters: should contain defaults (C=1, kernel="rbf") after buildHyperparametersPayload
    // We don't overfit to exact shape beyond key values.
    expect(receivedPayload.hyperparameters).toMatchObject({
      C: 1,
      kernel: "rbf",
    });

    // --- Assert: redirected to home ---
    expect(await screen.findByText("HOME")).toBeInTheDocument();

    scrollSpy.mockRestore();
  });
});
