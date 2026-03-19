import { useState } from "react";
import api from "../api";
import { Link, useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

import ErrorBanner from "./UI/ErrorBanner";

function getAuthErrorMessage(error, method) {
  const data = error?.response?.data;

  if (typeof data?.detail === "string" && data.detail.trim()) {
    return data.detail;
  }

  if (data && typeof data === "object") {
    for (const value of Object.values(data)) {
      if (Array.isArray(value) && value.length > 0) {
        return String(value[0]);
      }

      if (typeof value === "string" && value.trim()) {
        return value;
      }
    }
  }

  return method === "login"
    ? "Login failed. Check your credentials and try again."
    : "Registration failed. Please try again.";
}

function Form({ route, method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const title = method === "login" ? "Login" : "Register";

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(route, { username, password });
      if (method === "login") {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch (error) {
      setErrorMsg(getAuthErrorMessage(error, method));
    } finally {
      setLoading(false);
    }
  };

  function handleUsernameChange(e) {
    setUsername(e.target.value);
    if (errorMsg) setErrorMsg("");
  }

  function handlePasswordChange(e) {
    setPassword(e.target.value);
    if (errorMsg) setErrorMsg("");
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 to-slate-800 px-4">
      {/* === MAIN TITLE === */}
      <h1 className="mb-12 text-center text-5xl md:text-6xl font-extrabold tracking-tight text-white">
        <span className="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
          Machine Learning
        </span>
        <br />
        <span className="text-slate-300">Algorithms Playground</span>
      </h1>

      {/* === FORM === */}
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-slate-900/80 backdrop-blur border border-slate-700 rounded-2xl shadow-xl p-8 space-y-6"
      >
        <h2 className="text-3xl font-bold text-center text-white">{title}</h2>

        <ErrorBanner message={errorMsg} />

        <div className="space-y-4">
          <input
            className="w-full px-4 py-3 rounded-lg bg-slate-800 text-white placeholder-slate-400 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
            type="text"
            value={username}
            onChange={handleUsernameChange}
            placeholder="Username"
            required
          />

          <input
            className="w-full px-4 py-3 rounded-lg bg-slate-800 text-white placeholder-slate-400 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
            type="password"
            value={password}
            onChange={handlePasswordChange}
            placeholder="Password"
            required
          />
        </div>

        <button
          className="w-full py-3 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
          type="submit"
          disabled={loading}
        >
          {loading ? "Loading..." : title}
        </button>
        <div className="text-center text-sm text-slate-400">
          {method === "login" ? (
            <>
              Don&apos;t have an account?{" "}
              <Link
                to="/register"
                className="font-medium text-cyan-300 transition hover:text-cyan-200"
              >
                Register
              </Link>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <Link
                to="/login"
                className="font-medium text-cyan-300 transition hover:text-cyan-200"
              >
                Login
              </Link>
            </>
          )}
        </div>
      </form>
    </div>
  );
}

export default Form;
