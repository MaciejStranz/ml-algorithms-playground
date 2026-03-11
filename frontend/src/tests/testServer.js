import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/datasets/", () => HttpResponse.json([])),
  http.get("/api/algorithms/", () => HttpResponse.json([])),
  http.get("/api/experiments/", () => HttpResponse.json([])),
];

export const server = setupServer(...handlers);
export { http, HttpResponse };
