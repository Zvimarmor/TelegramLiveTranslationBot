def build_translation_prompt(original_text: str, sender_id: str, languages: list[str]) -> str:
    """
    Build a formatted prompt to send to the LLM for translation.
    
    Args:
        original_text (str): The message sent in the WhatsApp group.
        sender_id (str): The (anonymized) sender ID or nickname.
        languages (list[str]): List of language names to translate into.

    Returns:
        str: A structured prompt string for the LLM.
    """
    prompt = f"""
You are a translation assistant helping a multilingual WhatsApp group understand each other.

A user (ID: {sender_id}) sent the following message:
"{original_text}"

Please translate this message into the following languages. For each, include the language name and the translation in this format:

- [Language Name]: [Translated Message]

Languages to translate into:
{', '.join(languages)}
"""
    return prompt.strip()
