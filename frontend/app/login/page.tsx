"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import Logo from "@/components/logo";
import { loginUser } from "@/lib/api";


export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);


  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data = await loginUser(
        email,
        password,
      );

      localStorage.setItem(
        "access_token",
        data.access_token,
      );

      router.push("/dashboard");
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to sign in",
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <main className="relative flex min-h-screen overflow-hidden">

      {/* Background glow */}
      <div className="pointer-events-none absolute left-1/4 top-0 h-96 w-96 rounded-full bg-indigo-600/10 blur-3xl" />

      <div className="pointer-events-none absolute bottom-0 right-0 h-96 w-96 rounded-full bg-violet-600/10 blur-3xl" />


      {/* Left panel */}
      <section className="relative hidden w-1/2 flex-col justify-between border-r border-white/5 p-12 lg:flex">

        <Logo />

        <div className="max-w-xl">

          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-400/20 bg-indigo-400/10 px-3 py-1.5 text-xs font-medium text-indigo-300">
            <span className="h-1.5 w-1.5 rounded-full bg-indigo-400" />
            AI-powered engineering intelligence
          </div>

          <h1 className="text-5xl font-semibold leading-tight tracking-tight text-white">
            Understand your
            <span className="block bg-gradient-to-r from-indigo-400 via-violet-400 to-cyan-400 bg-clip-text text-transparent">
              codebase.
            </span>
          </h1>

          <p className="mt-6 max-w-lg text-lg leading-8 text-slate-400">
            Connect your repositories, explore your architecture,
            and ask questions about your code using AI grounded
            in your actual engineering knowledge.
          </p>

          <div className="mt-10 grid grid-cols-3 gap-3">

            {[
              ["01", "Index"],
              ["02", "Understand"],
              ["03", "Ask"],
            ].map(([number, label]) => (
              <div
                key={number}
                className="rounded-2xl border border-white/5 bg-white/[0.025] p-4"
              >
                <div className="text-xs text-slate-600">
                  {number}
                </div>

                <div className="mt-2 text-sm font-medium text-slate-300">
                  {label}
                </div>
              </div>
            ))}

          </div>
        </div>

        <p className="text-xs text-slate-600">
          CodeMind · Engineering Intelligence Platform
        </p>
      </section>


      {/* Login panel */}
      <section className="relative flex w-full items-center justify-center p-6 lg:w-1/2">

        <div className="w-full max-w-md">

          <div className="mb-8 lg:hidden">
            <Logo />
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-semibold tracking-tight text-white">
              Welcome back
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Sign in to continue to CodeMind.
            </p>
          </div>


          <form
            onSubmit={handleSubmit}
            className="space-y-5"
          >

            <div>
              <label
                htmlFor="email"
                className="mb-2 block text-sm font-medium text-slate-300"
              >
                Email
              </label>

              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                required
                className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.035] px-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-indigo-500/60 focus:bg-white/[0.05] focus:ring-4 focus:ring-indigo-500/10"
              />
            </div>


            <div>
              <div className="mb-2 flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="text-sm font-medium text-slate-300"
                >
                  Password
                </label>

                <button
                  type="button"
                  className="text-xs text-indigo-400 transition hover:text-indigo-300"
                >
                  Forgot password?
                </button>
              </div>

              <input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                required
                className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.035] px-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-indigo-500/60 focus:bg-white/[0.05] focus:ring-4 focus:ring-indigo-500/10"
              />
            </div>


            {error && (
              <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                {error}
              </div>
            )}


            <button
              type="submit"
              disabled={loading}
              className="group relative h-12 w-full overflow-hidden rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 text-sm font-semibold text-white shadow-lg shadow-indigo-500/20 transition hover:from-indigo-400 hover:to-violet-500 hover:shadow-indigo-500/30 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <span className="relative z-10">
                {loading
                  ? "Signing in..."
                  : "Sign in"}
              </span>
            </button>

          </form>


          <div className="my-8 flex items-center gap-4">
            <div className="h-px flex-1 bg-white/5" />
            <span className="text-xs text-slate-600">
              CodeMind
            </span>
            <div className="h-px flex-1 bg-white/5" />
          </div>


          <p className="text-center text-sm text-slate-500">
            AI-powered software engineering intelligence
          </p>

        </div>
      </section>

    </main>
  );
}