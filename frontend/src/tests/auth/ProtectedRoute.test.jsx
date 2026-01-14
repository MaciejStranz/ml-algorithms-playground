import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { http, HttpResponse } from "../testServer";
import { server } from "../testServer";

import ProtectedRoute from "../../components/ProtectedRoute";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constants";


/**
 * Simple component used as protected content.
 */
function SecretPage() {
  return <div>SECRET</div>;
}

/**
 * Minimal login page used to verify redirects.
 */
function LoginPage() {
  return <div>LOGIN</div>;
}

/**
 * Creates a fake JWT in the format header.payload.signature.
 * jwt-decode does not verify the signature, it only decodes the payload.
 */
function createJwtWithExp(expSeconds) {
  const payload = { exp: expSeconds };
  return `header.${btoa(JSON.stringify(payload))}.signature`;
}

function createValidJwt({ minutes = 10 } = {}) {
  const exp = Math.floor(Date.now() / 1000) + minutes * 60;
  return createJwtWithExp(exp);
}

function createExpiredJwt({ minutesAgo = 10 } = {}) {
  const exp = Math.floor(Date.now() / 1000) - minutesAgo * 60;
  return createJwtWithExp(exp);
}

/**
 * Helper for rendering a minimal router with ProtectedRoute.
 */
function renderProtectedApp(initialPath = "/") {
  render(
    <MemoryRouter initialEntries={[initialPath]}>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <SecretPage />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </MemoryRouter>
  );
}

describe("ProtectedRoute", () => {
  beforeEach(() => {
    // Ensure a clean auth state before each test.
    localStorage.clear();
  });

  it("redirects to /login when no access token is present", async () => {
    // No ACCESS_TOKEN in localStorage -> should redirect
    renderProtectedApp("/");

    expect(await screen.findByText("LOGIN")).toBeInTheDocument();
    expect(screen.queryByText("SECRET")).not.toBeInTheDocument();
  });

  it("renders protected content when access token is valid", async () => {
    localStorage.setItem(ACCESS_TOKEN, createValidJwt());

    renderProtectedApp("/");

    expect(await screen.findByText("SECRET")).toBeInTheDocument();
    expect(screen.queryByText("LOGIN")).not.toBeInTheDocument();
  });

  it("refreshes token when access token is expired and refresh succeeds", async () => {
    // Put an expired access token and a refresh token in localStorage
    localStorage.setItem(ACCESS_TOKEN, createExpiredJwt());
    localStorage.setItem(REFRESH_TOKEN, "dummy-refresh-token");

    // Mock the refresh endpoint to return a new access token
    // Note: This assumes your api.post hits "/api/token/refresh/"
    const newAccess = createValidJwt({ minutes: 30 });
    const refreshUrl = "http://localhost:8000/api/token/refresh/";

    server.use(
      http.options(refreshUrl, () => new HttpResponse(null, { status: 204 })),
      http.post(refreshUrl, async () => {
        return HttpResponse.json({ access: newAccess }, { status: 200 });
      })
    );

    renderProtectedApp("/");

    // After refresh succeeds, protected content should be visible
    expect(await screen.findByText("SECRET")).toBeInTheDocument();
    expect(screen.queryByText("LOGIN")).not.toBeInTheDocument();

    // And localStorage should contain the refreshed access token
    expect(localStorage.getItem(ACCESS_TOKEN)).toBe(newAccess);
  });
});
