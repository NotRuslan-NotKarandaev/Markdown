"""Operations over strings."""


def rreplace(s, old, new, count):
    """Replaces old patterns of
    string from right side with new patterns
    the specified number of times."""
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]
