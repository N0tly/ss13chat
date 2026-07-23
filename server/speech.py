def get_speech(text: str) -> str:
    text = text.rstrip()

    if text.endswith("!!"):
        return "кричит"

    if text.endswith("!"):
        return "восклицает"

    if text.endswith("?"):
        return "спрашивает"

    return "говорит"