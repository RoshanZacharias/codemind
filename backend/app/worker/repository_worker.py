import asyncio
import json
import shutil
import tempfile
from pathlib import Path

import aio_pika
from sqlalchemy import update

from ..config import settings
from ..database import AsyncSessionLocal
from ..models.repository import Repository
from ..models.repository_file import RepositoryFile
from ..ingestion.chunk_service import (
    create_chunks_for_repository,
)


QUEUE_NAME = "repository_ingestion"

MAX_FILE_SIZE = 500 * 1024

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    ".next",
    "coverage",
}

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".java": "java",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".sql": "sql",
    ".md": "markdown",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
}


async def update_repository_status(
    repository_id: int,
    status: str,
) -> None:
    async with AsyncSessionLocal() as db:
        await db.execute(
            update(Repository)
            .where(Repository.id == repository_id)
            .values(status=status)
        )

        await db.commit()


def discover_files(repository_path: Path) -> list[Path]:
    discovered_files = []

    for path in repository_path.rglob("*"):
        if not path.is_file():
            continue

        relative_path = path.relative_to(repository_path)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        discovered_files.append(path)

    return discovered_files


def read_file_content(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_SIZE:
            return None

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    except (OSError, UnicodeError):
        return None


async def store_repository_files(
    repository_id: int,
    repository_path: Path,
) -> int:
    files = discover_files(repository_path)

    stored_count = 0

    async with AsyncSessionLocal() as db:
        for file_path in files:
            content = read_file_content(file_path)

            if content is None:
                continue

            relative_path = file_path.relative_to(
                repository_path
            )

            language = SUPPORTED_EXTENSIONS.get(
                file_path.suffix.lower()
            )

            repository_file = RepositoryFile(
                repository_id=repository_id,
                path=str(relative_path).replace("\\", "/"),
                language=language,
                size=file_path.stat().st_size,
                content=content,
            )

            db.add(repository_file)

            stored_count += 1

        await db.commit()

    return stored_count


async def clone_repository(
    repository_id: int,
    repository_url: str,
    branch: str,
) -> None:
    temp_directory = Path(
        tempfile.mkdtemp(
            prefix=f"codemind_repo_{repository_id}_"
        )
    )

    try:
        await update_repository_status(
            repository_id,
            "processing",
        )

        destination = temp_directory / "repository"

        process = await asyncio.create_subprocess_exec(
            "git",
            "clone",
            "--branch",
            branch,
            "--single-branch",
            repository_url,
            str(destination),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_message = stderr.decode(
                errors="replace"
            )

            print(
                f"Failed to clone repository {repository_id}: "
                f"{error_message}"
            )

            await update_repository_status(
                repository_id,
                "failed",
            )

            return

        print(
            f"Repository {repository_id} cloned successfully "
            f"to {destination}"
        )

        stored_count = await store_repository_files(
            repository_id=repository_id,
            repository_path=destination,
        )

        print(
            f"Repository {repository_id}: "
            f"stored {stored_count} files"
        )

        chunk_count = await create_chunks_for_repository(
            repository_id
        )

        print(
            f"Repository {repository_id}: "
            f"created {chunk_count} chunks"
        )

        await update_repository_status(
            repository_id,
            "completed",
        )

    except Exception as exc:
        print(
            f"Unexpected error processing repository "
            f"{repository_id}: {exc}"
        )

        await update_repository_status(
            repository_id,
            "failed",
        )

    finally:
        shutil.rmtree(
            temp_directory,
            ignore_errors=True,
        )


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        data = json.loads(
            message.body.decode()
        )

        repository_id = data["repository_id"]

        async with AsyncSessionLocal() as db:
            repository = await db.get(
                Repository,
                repository_id,
            )

        if repository is None:
            print(
                f"Repository {repository_id} does not exist"
            )
            return

        await clone_repository(
            repository_id=repository.id,
            repository_url=repository.url,
            branch=repository.branch,
        )


async def main() -> None:
    connection = await aio_pika.connect_robust(
        settings.rabbitmq_url
    )

    channel = await connection.channel()

    await channel.set_qos(
        prefetch_count=1
    )

    queue = await channel.declare_queue(
        QUEUE_NAME,
        durable=True,
    )

    print(
        f"Repository worker started. "
        f"Waiting for messages on '{QUEUE_NAME}'..."
    )

    await queue.consume(process_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())