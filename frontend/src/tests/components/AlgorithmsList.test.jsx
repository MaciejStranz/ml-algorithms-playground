import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, expect, test } from "vitest";
import { http, HttpResponse } from "msw";

import { server } from "../testServer";
import AlgorithmsList from "../../components/Algorithms/AlgorithmsList";

const ALGORITHMS_URL = /\/api\/algorithms\/$/;

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
      <AlgorithmsList />
    </QueryClientProvider>
  );
}

describe("AlgorithmsList", () => {
  test("shows loading state while fetching algorithms", async () => {
    server.use(
      http.get(ALGORITHMS_URL, async () => {
        await new Promise((r) => setTimeout(r, 150));
        return HttpResponse.json([], { status: 200 });
      })
    );

    renderList();

    expect(screen.getByText(/loading algorithms/i)).toBeInTheDocument();
    expect(await screen.findByText(/no algorithms available/i)).toBeInTheDocument();
  });

  test("renders algorithms using new API contract (variants + supported_tasks)", async () => {
    server.use(
      http.get(ALGORITHMS_URL, () =>
        HttpResponse.json(
          [
            {
              id: 1,
              code: "svm",
              name: "Support Vector Machine",
              kind: "classical",
              description: "Support Vector Machine classifier/regressor.",
              variants: [
                {
                  id: 101,
                  code: "svc",
                  supported_tasks: ["binary_classification", "multiclass_classification"],
                  hyperparameter_specs: [{ name: "C", type: "float", default: 1.0 }],
                },
                {
                  id: 102,
                  code: "svr",
                  supported_tasks: ["regression"],
                  hyperparameter_specs: [{ name: "epsilon", type: "float", default: 0.1 }],
                },
              ],
            },
          ],
          { status: 200 }
        )
      )
    );

    renderList();

    expect(
      await screen.findByRole("heading", { name: /support vector machine/i })
    ).toBeInTheDocument();

    expect(screen.getByText(/supported tasks:/i)).toBeInTheDocument();
    expect(screen.getByText(/available variants:/i)).toBeInTheDocument();

    // tasks are formatted in UI: "_" -> " "
    expect(screen.getByText(/binary classification/i)).toBeInTheDocument();
    expect(screen.getByText(/multiclass classification/i)).toBeInTheDocument();
    expect(screen.getByText(/regression/i)).toBeInTheDocument();

    // variant code badges
    expect(screen.getByText("svc")).toBeInTheDocument();
    expect(screen.getByText("svr")).toBeInTheDocument();
  });

  test("shows empty state when no algorithms are available", async () => {
    server.use(
      http.get(ALGORITHMS_URL, () => HttpResponse.json([], { status: 200 }))
    );

    renderList();

    expect(await screen.findByText(/no algorithms available/i)).toBeInTheDocument();
  });

  test("shows backend error message when request fails", async () => {
    server.use(
      http.get(ALGORITHMS_URL, () =>
        HttpResponse.json({ detail: "Backend unavailable." }, { status: 500 })
      )
    );

    renderList();

    expect(await screen.findByText(/backend unavailable/i)).toBeInTheDocument();
  });
});
