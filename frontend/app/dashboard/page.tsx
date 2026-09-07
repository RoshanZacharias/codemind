"use client";

import { useEffect, useState } from "react";

import {
  createProject,
  getProjects,
} from "@/lib/api";

import Logo from "@/components/logo";


type Project = {
  id: number;
  name: string;
  description: string | null;
  user_id: number;
  created_at: string;
};


export default function DashboardPage() {

  const [projects, setProjects] = useState<Project[]>([]);

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");



  async function loadProjects() {

    const token =
      localStorage.getItem("access_token");

    if (!token) {
      window.location.href = "/login";
      return;
    }

    try {

      const data = await getProjects(token);

      setProjects(data);

    } catch (error) {

      setError(
        error instanceof Error
          ? error.message
          : "Failed to load projects",
      );

    } finally {

      setLoading(false);

    }
  }



  useEffect(() => {
    loadProjects();
  }, []);



  async function handleCreateProject() {

    const token =
      localStorage.getItem("access_token");

    if (!token) {
      window.location.href = "/login";
      return;
    }

    if (!name.trim()) {
      return;
    }

    setCreating(true);
    setError("");

    try {

      const project =
        await createProject(
          token,
          name,
          description,
        );

      setProjects((current) => [
        project,
        ...current,
      ]);

      setName("");
      setDescription("");

    } catch (error) {

      setError(
        error instanceof Error
          ? error.message
          : "Failed to create project",
      );

    } finally {

      setCreating(false);

    }
  }



  function logout() {

    localStorage.removeItem(
      "access_token",
    );

    window.location.href = "/login";
  }



  return (
    <div className="min-h-screen bg-[#070a13] text-slate-200">

      {/* Top navigation */}
      <header className="sticky top-0 z-20 border-b border-white/5 bg-[#070a13]/80 backdrop-blur-xl">

        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">

          <Logo />

          <div className="flex items-center gap-4">

            <div className="hidden text-right sm:block">
              <p className="text-sm font-medium text-slate-200">
                Developer
              </p>

              <p className="text-xs text-slate-500">
                CodeMind workspace
              </p>
            </div>

            <button
              onClick={logout}
              className="rounded-lg border border-white/10 px-3 py-2 text-xs font-medium text-slate-400 transition hover:border-white/20 hover:text-white"
            >
              Logout
            </button>

          </div>

        </div>

      </header>


      <main className="mx-auto max-w-7xl px-6 py-10">

        {/* Hero */}
        <section className="mb-10">

          <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">

            <div>

              <div className="mb-3 flex items-center gap-2 text-xs font-medium text-indigo-400">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-400" />
                Workspace
              </div>

              <h1 className="text-4xl font-semibold tracking-tight text-white">
                Your engineering workspace
              </h1>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">
                Explore repositories, understand architecture,
                and ask AI questions grounded in your codebase.
              </p>

            </div>

            <button
              onClick={() =>
                document
                  .getElementById("create-project")
                  ?.scrollIntoView({
                    behavior: "smooth",
                  })
              }
              className="rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/10 transition hover:from-indigo-400 hover:to-violet-500"
            >
              + New project
            </button>

          </div>

        </section>


        {/* Stats */}
        <section className="mb-10 grid gap-4 sm:grid-cols-3">

          {[
            {
              label: "Projects",
              value: projects.length,
              icon: "◈",
            },
            {
              label: "Repositories",
              value: "—",
              icon: "⌘",
            },
            {
              label: "AI queries",
              value: "—",
              icon: "✦",
            },
          ].map((stat) => (

            <div
              key={stat.label}
              className="group rounded-2xl border border-white/[0.07] bg-white/[0.025] p-5 transition hover:border-indigo-500/20 hover:bg-white/[0.035]"
            >

              <div className="flex items-center justify-between">

                <span className="text-xs font-medium uppercase tracking-wider text-slate-600">
                  {stat.label}
                </span>

                <span className="text-indigo-400/70">
                  {stat.icon}
                </span>

              </div>

              <p className="mt-4 text-3xl font-semibold tracking-tight text-white">
                {stat.value}
              </p>

            </div>

          ))}

        </section>


        <div className="grid gap-8 lg:grid-cols-[1fr_380px]">

          {/* Projects */}
          <section>

            <div className="mb-5 flex items-center justify-between">

              <div>
                <h2 className="text-lg font-semibold text-white">
                  Your projects
                </h2>

                <p className="mt-1 text-xs text-slate-600">
                  Engineering knowledge bases
                </p>
              </div>

              <span className="rounded-full border border-white/5 bg-white/[0.025] px-3 py-1 text-xs text-slate-500">
                {projects.length} total
              </span>

            </div>


            {loading && (
              <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-8 text-center text-sm text-slate-500">
                Loading workspace...
              </div>
            )}


            {!loading && projects.length === 0 && (

              <div className="rounded-2xl border border-dashed border-white/10 bg-white/[0.015] p-12 text-center">

                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-500/10 text-xl text-indigo-400">
                  ◈
                </div>

                <h3 className="mt-5 font-medium text-white">
                  No projects yet
                </h3>

                <p className="mx-auto mt-2 max-w-sm text-sm leading-6 text-slate-600">
                  Create your first project and connect a repository
                  to start building your engineering knowledge base.
                </p>

              </div>

            )}


            <div className="space-y-3">

              {projects.map((project) => (

                <div
                  key={project.id}
                  className="group flex cursor-pointer items-center justify-between rounded-2xl border border-white/[0.07] bg-white/[0.025] p-5 transition hover:-translate-y-0.5 hover:border-indigo-500/25 hover:bg-white/[0.04]"
                >

                  <div className="flex items-center gap-4">

                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500/20 to-violet-500/10 text-indigo-400">
                      ◈
                    </div>

                    <div>

                      <h3 className="font-medium text-white">
                        {project.name}
                      </h3>

                      <p className="mt-1 max-w-lg text-sm text-slate-600">
                        {project.description ||
                          "No description provided"}
                      </p>

                    </div>

                  </div>

                  <span className="ml-4 text-lg text-slate-700 transition group-hover:text-indigo-400">
                    →
                  </span>

                </div>

              ))}

            </div>

          </section>


          {/* Create project */}
          <section
            id="create-project"
            className="h-fit rounded-2xl border border-white/[0.07] bg-white/[0.025] p-6"
          >

            <div className="mb-6">

              <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400">
                +
              </div>

              <h2 className="text-lg font-semibold text-white">
                Create project
              </h2>

              <p className="mt-1 text-sm leading-6 text-slate-600">
                Start a new engineering knowledge base.
              </p>

            </div>


            <div className="space-y-4">

              <div>

                <label className="mb-2 block text-xs font-medium text-slate-400">
                  Project name
                </label>

                <input
                  type="text"
                  placeholder="e.g. CodeMind API"
                  value={name}
                  onChange={(event) =>
                    setName(event.target.value)
                  }
                  className="h-11 w-full rounded-xl border border-white/10 bg-black/20 px-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10"
                />

              </div>


              <div>

                <label className="mb-2 block text-xs font-medium text-slate-400">
                  Description
                </label>

                <textarea
                  placeholder="What are you building?"
                  value={description}
                  onChange={(event) =>
                    setDescription(event.target.value)
                  }
                  rows={4}
                  className="w-full resize-none rounded-xl border border-white/10 bg-black/20 px-3 py-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-indigo-500/50 focus:ring-4 focus:ring-indigo-500/10"
                />

              </div>


              {error && (
                <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-3 py-3 text-xs text-red-300">
                  {error}
                </div>
              )}


              <button
                onClick={handleCreateProject}
                disabled={creating || !name.trim()}
                className="h-11 w-full rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 text-sm font-semibold text-white shadow-lg shadow-indigo-500/10 transition hover:from-indigo-400 hover:to-violet-500 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {creating
                  ? "Creating..."
                  : "Create project"}
              </button>

            </div>

          </section>

        </div>

      </main>

    </div>
  );
}