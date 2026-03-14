import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";

import api from "../api";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants";

function ProtectedRoute({ children }) {
  const [isAuthorized, setIsAuthorized] = useState(null);

  useEffect(() => {
    async function refreshToken() {
      const refresh = localStorage.getItem(REFRESH_TOKEN);

      if (!refresh) {
        setIsAuthorized(false);
        return;
      }

      try {
        const res = await api.post("/api/token/refresh/", { refresh });
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        setIsAuthorized(true);
      } catch {
        setIsAuthorized(false);
      }
    }

    async function auth() {
      const token = localStorage.getItem(ACCESS_TOKEN);

      if (!token) {
        setIsAuthorized(false);
        return;
      }

      try {
        const decoded = jwtDecode(token);
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000;

        if (tokenExpiration < now) {
          await refreshToken();
        } else {
          setIsAuthorized(true);
        }
      } catch {
        setIsAuthorized(false);
      }
    }

    auth();
  }, []);

  if (isAuthorized === null) {
    return <div>Loading...</div>;
  }

  return isAuthorized ? children : <Navigate to="/login" replace />;
}

export default ProtectedRoute;
