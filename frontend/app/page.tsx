import Link from "next/link";

import Logo from "@/components/logo";


export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden">

      {/* Ambient background */}
      <div className="pointer-events-none absolute left-1/2 top-0 h-[600px] w-[800px] -translate-x-1/2 rounded-full bg-indigo-600/10 blur-3xl" />

      <div className="relative mx-auto max-w-6xl px-6">

        {/* Navbar */}
        <nav className="flex h-20 items-center justify-between">

          <Logo />

          <div className="flex items-center gap-3">

            <Link
              href="/login"
              className="rounded-lg px-4 py-2 text-sm text-slate-400 transition hover:text-white"
            >
              Sign in
            </Link>

            <Link
              href="/login"
              className="rounded-xl bg-white px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-slate-200"
            >
              Get started
            </Link>

          </div>

        </nav>


        {/* Hero */}
        <section className="flex min-h-[calc(100vh-80px)] flex-col items-center justify-center pb-20 text-center">

          <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-indigo-400/20 bg-indigo-400/10 px-4 py-2 text-xs font-medium text-indigo-300">

            <span className="h-1.5 w-1.5 rounded-full bg-indigo-400" />

            AI-powered software engineering intelligence

          </div>


          <h1 className="max-w-4xl text-5xl font-semibold leading-[1.05] tracking-tight text-white sm:text-6xl lg:text-7xl">

            Your codebase has answers.

            <span className="block bg-gradient-to-r from-indigo-400 via-violet-400 to-cyan-400 bg-clip-text text-transparent">
              CodeMind finds them.
            </span>

          </h1>


          <p className="mt-7 max-w-2xl text-base leading-7 text-slate-500 sm:text-lg">

            Connect your repositories and technical knowledge.
            Search your code semantically, understand architecture,
            and ask questions using AI grounded in your actual codebase.

          </p>


          <div className="mt-10 flex flex-col gap-3 sm:flex-row">

            <Link
              href="/login"
              className="rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 px-6 py-3.5 text-sm font-semibold text-white shadow-xl shadow-indigo-500/20 transition hover:from-indigo-400 hover:to-violet-500"
            >
              Start building →
            </Link>

            <a
              href="#features"
              className="rounded-xl border border-white/10 bg-white/[0.025] px-6 py-3.5 text-sm font-medium text-slate-300 transition hover:border-white/20 hover:bg-white/[0.05]"
            >
              Explore the platform
            </a>

          </div>


          {/* Product preview */}
          <div
            id="features"
            className="mt-20 w-full max-w-5xl rounded-2xl border border-white/[0.08] bg-white/[0.025] p-2 shadow-2xl shadow-black/40"
          >

            <div className="rounded-xl border border-white/5 bg-[#0b1020] p-6 text-left">

              <div className="mb-6 flex items-center gap-2">

                <span className="h-2.5 w-2.5 rounded-full bg-red-400/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-yellow-400/70" />
                <span className="h-2.5 w-2.5 rounded-full bg-green-400/70" />

              </div>


              <div className="grid gap-4 md:grid-cols-[180px_1fr]">

                <div className="space-y-2 border-r border-white/5 pr-4">

                  {[
                    "Dashboard",
                    "Repositories",
                    "Documents",
                    "AI Chat",
                  ].map((item, index) => (

                    <div
                      key={item}
                      className={`rounded-lg px-3 py-2 text-xs ${
                        index === 0
                          ? "bg-indigo-500/10 text-indigo-300"
                          : "text-slate-600"
                      }`}
                    >
                      {item}
                    </div>

                  ))}

                </div>


                <div>

                  <p className="text-xs text-slate-600">
                    CODEMIND / PROJECT
                  </p>

                  <h3 className="mt-2 text-xl font-medium text-white">
                    Engineering workspace
                  </h3>

                  <div className="mt-6 grid gap-3 sm:grid-cols-3">

                    {[
                      ["12", "Files indexed"],
                      ["48", "Code chunks"],
                      ["128", "AI queries"],
                    ].map(([value, label]) => (

                      <div
                        key={label}
                        className="rounded-xl border border-white/5 bg-white/[0.02] p-4"
                      >

                        <p className="text-xl font-semibold text-white">
                          {value}
                        </p>

                        <p className="mt-1 text-xs text-slate-600">
                          {label}
                        </p>

                      </div>

                    ))}

                  </div>

                </div>

              </div>

            </div>

          </div>

        </section>

      </div>

    </main>
  );
}