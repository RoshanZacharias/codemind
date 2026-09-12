"use client";

import { FormEvent, use, useState } from "react";
import { askRepository, AskResponse } from "@/lib/api";
import ReactMarkdown from "react-markdown";

export default function RepositoryPage({
  params,
}: {
  params: Promise<{ repositoryId: string }>;
}) {
  const { repositoryId: repositoryIdString } = use(params);
  const repositoryId = Number(repositoryIdString);

  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const result = await askRepository(
        repositoryId,
        question.trim(),
      );

      setResponse(result);
      setQuestion("");
    } catch (err) {
      console.error(err);
      setError("Something went wrong while asking the repository.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            CodeMind
          </h1>

          <p className="mt-2 text-gray-600">
            Ask questions about your repository.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-3">
            <input
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="How does authentication work?"
              disabled={loading}
              className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 outline-none focus:border-blue-500"
            />

            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>
        </form>

        {error && (
          <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {response && (
          <div className="space-y-6">
            <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-semibold text-gray-900">
                Answer
              </h2>

              <div className="max-w-none text-gray-700">
                <ReactMarkdown>
                  {response.answer}
                </ReactMarkdown>
              </div>
            </section>

            <section className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-semibold text-gray-900">
                Sources
              </h2>

              <div className="space-y-3">
                {response.sources.map((source, index) => (
                  <div
                    key={`${source.file}-${source.start_line}-${index}`}
                    className="rounded-lg border border-gray-200 p-4"
                  >
                    <div className="font-mono text-sm font-medium text-gray-900">
                      {source.file}
                    </div>

                    <div className="mt-1 text-sm text-gray-500">
                      Lines {source.start_line}-{source.end_line}
                      {source.language &&
                        ` • ${source.language}`}
                    </div>

                    
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}
      </div>
    </main>
  );
}