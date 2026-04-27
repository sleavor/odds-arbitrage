def normalize_event(name: str) -> str:
    """
    Normalizes event/selection names for consistent matching across clients.
    """
    if not name:
        return ""
    return " ".join(name.strip().lower().split())