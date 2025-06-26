import os
import logging
import requests

# You can switch to another LLM provider by replacing this logic
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # Options: "openai", "grok", "mock"

# Example environment variable if you use OpenAI or Grok
LLM_API_KEY = os.getenv("LLM_API_KEY")

def translate_with_llm(prompt: str) -> str:
    """
    Sends the prompt to the configured LLM and returns the response text.

    Args:
        prompt (str): The constructed prompt from prompt_builder.

    Returns:
        str: The translated message block as returned by the LLM.
    """
    logging.info(f"Sending prompt to LLM ({LLM_PROVIDER})...")

    if LLM_PROVIDER == "mock":
        return _mock_translation(prompt)

    elif LLM_PROVIDER == "grok":
        return _call_grok(prompt)

    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def _call_openai(prompt: str) -> str:
    import openai

    openai.api_key = LLM_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.5
    )
    return response["choices"][0]["message"]["content"].strip()

def _call_grok(prompt: str) -> str:
    """
    Placeholder for Grok API integration.
    """
    raise NotImplementedError("Grok integration not yet implemented")

def _mock_translation(prompt: str) -> str:
    """
    Mock function for testing without real API.
    """
    return (
        "- Arabic: كيف حالك؟\n"
        "- Hebrew: מה שלומך?\n"
        "- Spanish: ¿Cómo estás?\n"
    )
