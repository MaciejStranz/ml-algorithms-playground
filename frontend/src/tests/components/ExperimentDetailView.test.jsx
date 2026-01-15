import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Routes, Route, useParams } from "react-router-dom";
import { http, HttpResponse } from "msw";
import { server } from "../testServer";

// Adjust this path to your structure:
import ExperimentDetailView from "../../components/Experiments/ExperimentDetailView";

// Match both relative and absolute baseURL
const EXPERIMENT_DETAIL_URL = /\/api\/experiments\/\d+\/$/;

function DetailRouteWrapper() {
  const { id } = useParams();
  return <ExperimentDetailView experimentId={id} />;
}

function renderApp(initialEntry) {
  render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <Routes>
        <Route path="/" element={<div>HOME</div>} />
        <Route path="/experiments/:id" element={<DetailRouteWrapper />} />
      </Routes>
    </MemoryRouter>
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
            algorithm: { id: 1, name: "Support Vector Machine" },
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

    // Title
    expect(await screen.findByRole("heading", { name: /experiment #11/i })).toBeInTheDocument();

    // Key badges
    expect(screen.getByText("finished")).toBeInTheDocument();
    expect(screen.getByText("multiclass_classification")).toBeInTheDocument();
    expect(screen.getByText("Iris")).toBeInTheDocument();
    expect(screen.getByText("Support Vector Machine")).toBeInTheDocument();

    // Sections
    expect(screen.getByRole("heading", { name: /summary/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /hyperparameters/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /metrics/i })).toBeInTheDocument();

    // Summary: Accuracy label + formatted %
    expect(screen.getByText("Accuracy")).toBeInTheDocument();
    expect(screen.getByText("93.3%")).toBeInTheDocument();

    // Hyperparameters JSON is shown
    expect(screen.getByText(/"kernel": "rbf"/i)).toBeInTheDocument();
    expect(screen.getByText(/"C": 1/i)).toBeInTheDocument();

    // Metrics JSON is shown (contains accuracy)
    expect(screen.getByText(/"accuracy": 0\.933333/i)).toBeInTheDocument();
  });

  test("renders experiment details and shows R² for regression", async () => {
    server.use(
      http.get(EXPERIMENT_DETAIL_URL, () =>
        HttpResponse.json(
          {
            id: 7,
            dataset: { id: 5, name: "Sinusoid Function" },
            algorithm: { id: 5, name: "Neural Network (MLP, PyTorch)" },
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

    expect(await screen.findByRole("heading", { name: /experiment #7/i })).toBeInTheDocument();

    // Summary: R² label + toFixed(4)
    expect(screen.getByText("R²")).toBeInTheDocument();
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
            algorithm: { id: 1, name: "Support Vector Machine" },
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
        const parts = url.pathname.split("/").filter(Boolean); // ["api","experiments","11"]
        deletedId = Number(parts[2]);
        return new HttpResponse(null, { status: 204 });
      })
    );

    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);

    renderApp("/experiments/11");

    // Wait for content
    expect(await screen.findByRole("heading", { name: /experiment #11/i })).toBeInTheDocument();

    // Click delete
    await user.click(screen.getByRole("button", { name: /delete/i }));

    // Redirect to home
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

    // Error message
    expect(await screen.findByText(/not found/i)).toBeInTheDocument();

    // Link back exists and is correct
    const back = screen.getByRole("link", { name: /back to home/i });
    expect(back).toHaveAttribute("href", "/");
  });
});
