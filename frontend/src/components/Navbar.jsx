import { Link, NavLink, replace, useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

export default function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
    navigate("/login", { replace: true });
  }

  return (
    <header className="sticky top-0 z-50 border-b border-slate-700 bg-slate-900/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-2">
          <span className="text-lg font-extrabold text-white">
            ML Algorithms Playground
          </span>
        </Link>

        <nav className="flex items-center gap-3">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `rounded-lg px-3 py-2 text-sm font-semibold transition ${
                isActive
                  ? "text-white bg-slate-800"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/60"
              }`
            }
          >
            Home
          </NavLink>

          <NavLink
            to="/datasets"
            className={({ isActive }) =>
              `rounded-lg px-3 py-2 text-sm font-semibold transition ${
                isActive
                  ? "text-white bg-slate-800"
                  : "text-slate-300 hover:text-white hover:bg-slate-800/60"
              }`
            }
          >
            Datasets
          </NavLink>

          <NavLink
            to="/experiments/new"
            className={({ isActive }) =>
              `rounded-lg px-3 py-2 text-sm font-semibold transition ${
                isActive
                  ? "text-white bg-indigo-700"
                  : "bg-indigo-600 text-white hover:bg-indigo-700"
              }`
            }
          >
            Run experiment
          </NavLink>

          <button
            onClick={handleLogout}
            className="rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white hover:bg-red-700 transition cursor-pointer"
          >
            Logout
          </button>
        </nav>
      </div>
    </header>
  );
}
