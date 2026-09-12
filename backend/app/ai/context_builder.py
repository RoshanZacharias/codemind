def build_context(results: list[dict]) -> str:
    context_parts = []

    for result in results:
        context_parts.append(
            f"""
    File: {result["file_path"]}
    Language: {result["language"]}
    Lines: {result["start_line"]}-{result["end_line"]}

    ```{result["language"]}
    {result["content"]}

    """
    )

    return "\n".join(context_parts)