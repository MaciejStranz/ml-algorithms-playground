import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { http, HttpResponse } from "msw";
import { server } from "../testServer";

// Adjust this path if needed:
import ExperimentsList from "../../components/experiments/ExperimentsList";

/**
 * Match both:
 *  - "/api/experiments/"
 *  - "http://localhost:8000/api/experiments/"
 */
const EXPERIMENTS_LIST_URL = /\/api\/experiments\/$/;

/**
 * Match delete endpoint:
 *  - "/api/experiments/:id/"
 *  - "http://localhost:8000/api/experiments/:id/"
 */
const EXPERIMENT_DELETE_URL = /\/api\/experiments\/\d+\/$/;

function renderList() {
  render(
    <MemoryRouter initialEntries={["/"]}>
      <ExperimentsList />
    </MemoryRouter>
  );
}

describe("ExperimentsList", () => {
  test("shows a loading state while experiments are being fetched", async () => {
    server.use(
      http.get(EXPERIMENTS_LIST_URL, async () => {
        await new Promise((r) => setTimeout(r, 150));
        return HttpResponse.json([], { status: 200 });
      })
    );

    renderList();

    expect(screen.getByText(/loading experiments/i)).toBeInTheDocument();
    expect(await screen.findByText(/no experiments yet/i)).toBeInTheDocument();
  });

  test("renders experiments and displays Accuracy (%) for classification and R² for regression", async () => {
    server.use(
      http.get(EXPERIMENTS_LIST_URL, () =>
        HttpResponse.json(
          [
            {
              id: 11,
              dataset: { id: 1, name: "Iris" },
              algorithm: { id: 1, name: "Support Vector Machine" },
              task: "multiclass_classification",
              created_at: "2025-12-06T03:08:18.950169Z",
              status: "finished",
              hyperparameters: { C: 1, kernel: "rbf" },
              metrics: { accuracy: 0.9333333333333333 },
            },
            {
              id: 7,
              dataset: { id: 5, name: "Sinusoid Function" },
              algorithm: { id: 5, name: "Neural Network (MLP, PyTorch)" },
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

    // Basic content
    expect(await screen.findByText(/experiment #11/i)).toBeInTheDocument();
    expect(screen.getByText(/support vector machine/i)).toBeInTheDocument();
    expect(screen.getByText(/iris/i)).toBeInTheDocument();

    expect(screen.getByText(/experiment #7/i)).toBeInTheDocument();
    expect(screen.getByText(/sinusoid function/i)).toBeInTheDocument();

    // Metric mapping checks
    expect(screen.getByText(/93\.3%/)).toBeInTheDocument();     // Accuracy formatted as %
    expect(screen.getByText("R²")).toBeInTheDocument();         // R² label
    expect(screen.getByText(/0\.9986/)).toBeInTheDocument();    // R² value formatted to 4 decimals
  });

  test("shows an empty state when the user has no experiments", async () => {
    server.use(
      http.get(EXPERIMENTS_LIST_URL, () => HttpResponse.json([], { status: 200 }))
    );

    renderList();

    expect(await screen.findByText(/no experiments yet/i)).toBeInTheDocument();
  });

  test("deletes an experiment after confirmation and removes it from the list", async () => {
  const user = userEvent.setup();

  server.use(
    http.get(EXPERIMENTS_LIST_URL, () =>
      HttpResponse.json(
        [
          {
            id: 11,
            dataset: { id: 1, name: "Iris" },
            algorithm: { id: 1, name: "Support Vector Machine" },
            task: "multiclass_classification",
            created_at: "2025-12-06T03:08:18.950169Z",
            status: "finished",
            hyperparameters: {},
            metrics: { accuracy: 1.0 },
          },
          {
            id: 7,
            dataset: { id: 5, name: "Sinusoid Function" },
            algorithm: { id: 5, name: "Neural Network (MLP, PyTorch)" },
            task: "regression",
            created_at: "2025-12-06T02:09:41.798903Z",
            status: "finished",
            hyperparameters: {},
            metrics: { r2: 0.5 },
          },
        ],
        { status: 200 }
      )
    )
  );

  let deletedId = null;

  server.use(
    http.delete(EXPERIMENT_DELETE_URL, ({ request }) => {
      const url = new URL(request.url);
      const parts = url.pathname.split("/").filter(Boolean); // ["api","experiments","11"]
      deletedId = Number(parts[2]);
      return new HttpResponse(null, { status: 204 });
    })
  );

  const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);

  renderList();

  // Assert: both experiments are visible via their links
  const exp11Link = await screen.findByRole("link", { name: /experiment #11/i });
  expect(exp11Link).toHaveAttribute("href", "/experiments/11");

  const exp7Link = screen.getByRole("link", { name: /experiment #7/i });
  expect(exp7Link).toHaveAttribute("href", "/experiments/7");

  // Act: click Delete for experiment #11
  // Still safe to click the first delete button because list order is deterministic (API order)
  const deleteButtons = screen.getAllByRole("button", { name: /^delete$/i });
  await user.click(deleteButtons[0]);

  // Assert: experiment #11 disappears, #7 remains
  expect(screen.queryByRole("link", { name: /experiment #11/i })).not.toBeInTheDocument();
  expect(screen.getByRole("link", { name: /experiment #7/i })).toBeInTheDocument();

  expect(deletedId).toBe(11);

  confirmSpy.mockRestore();
});

});
