export default function Logo() {
  return (
    <div className="flex items-center gap-3">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 shadow-lg shadow-indigo-500/20">
        <span className="text-sm font-bold text-white">
          ◈
        </span>
      </div>

      <span className="text-lg font-semibold tracking-tight text-white">
        CodeMind
      </span>
    </div>
  );
}