from dataclasses import dataclass


@dataclass
class CodeChunkData:
    chunk_index: int
    start_line: int
    end_line: int
    content: str


def chunk_code(
    content: str,
    chunk_size: int = 80,
    overlap: int = 10,
) -> list[CodeChunkData]:
    lines = content.splitlines()

    if not lines:
        return []

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(lines):
        end = min(
            start + chunk_size,
            len(lines),
        )

        chunk_lines = lines[start:end]

        chunks.append(
            CodeChunkData(
                chunk_index=chunk_index,
                start_line=start + 1,
                end_line=end,
                content="\n".join(chunk_lines),
            )
        )

        chunk_index += 1

        if end >= len(lines):
            break

        start = end - overlap

    return chunks