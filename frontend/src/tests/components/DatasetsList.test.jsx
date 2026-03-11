import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, test } from "vitest";
import { http, HttpResponse } from "msw";

import { server } from "../testServer";
import DatasetsList from "../../components/Datasets/DatasetsList";

const DATASETS_URL = /\/api\/datasets\/$/;

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
      <DatasetsList />
    </QueryClientProvider>,
  );
}

describe("DatasetsList", () => {
  test("shows loading state while fetching datasets", async () => {
    server.use(
      http.get(DATASETS_URL, async () => {
        await new Promise((r) => setTimeout(r, 150));
        return HttpResponse.json([], { status: 200 });
      }),
    );

    renderList();

    expect(screen.getByText(/loading datasets/i)).toBeInTheDocument();
    expect(
      await screen.findByText(/no datasets available/i),
    ).toBeInTheDocument();
  });

  test("renders datasets from API", async () => {
    server.use(
      http.get(DATASETS_URL, async () =>
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
              class_labels: ["setosa", "versicolor", "virginica"],
              feature_names: [
                "sepal length",
                "sepal width",
                "petal length",
                "petal width",
              ],
              target_name: "class",
            },
            {
              id: 2,
              code: "diabetes",
              name: "Diabetes",
              task: "regression",
              n_samples: 442,
              n_features: 10,
              n_classes: null,
              class_labels: null,
              feature_names: ["age", "sex", "bmi", "bp"],
              target_name: "progression",
            },
          ],
          { status: 200 },
        ),
      ),
    );

    renderList();

    expect(
      await screen.findByRole("heading", { name: /iris/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: /diabetes/i }),
    ).toBeInTheDocument();

    expect(screen.getByText(/multiclass_classification/i)).toBeInTheDocument();
    expect(screen.getByText(/regression/i)).toBeInTheDocument();

    expect(screen.getByText(/class labels/i)).toBeInTheDocument();
    expect(
      screen.getByText(/setosa, versicolor, virginica/i),
    ).toBeInTheDocument();

    expect(screen.getByText(/target/i)).toBeInTheDocument();
    expect(screen.getByText(/progression/i)).toBeInTheDocument();
  });

  test("shows empty state when no datasets are available", async () => {
    server.use(
      http.get(DATASETS_URL, async () =>
        HttpResponse.json([], { status: 200 }),
      ),
    );

    renderList();

    expect(
      await screen.findByText(/no datasets available/i),
    ).toBeInTheDocument();
  });

  test("shows backend error message when request fails", async () => {
    server.use(
      http.get(DATASETS_URL, async () =>
        HttpResponse.json({ detail: "Backend unavailable." }, { status: 500 }),
      ),
    );

    renderList();

    expect(await screen.findByText(/backend unavailable/i)).toBeInTheDocument();
  });
});
