from groq import AsyncGroq

from ..config import settings


client = AsyncGroq(
    api_key=settings.groq_api_key,
)


MODEL = "openai/gpt-oss-20b"


async def generate_response(
    system_prompt: str,
    user_prompt: str,
) -> str:
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""