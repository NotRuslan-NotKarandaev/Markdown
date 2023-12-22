"""https://en.wikipedia.org/wiki/Markdown"""
from modules import array

class Tag:
    """A class that represents an opening and closing tag and
    a codeword that corresponds to them.

    This class has three attributes: start, end, and codeword.
    It also has a method called replace_in that replaces the codeword
    in a string with the tags.
    """

    def __init__(self, start: str, end: str, codeword: str):
        """Initializes the Tag object with the given arguments.

        Args:
            start (str): The opening tag.
            end (str): The closing tag.
            codeword (str): The codeword that will be replaced by the tags.
        """
        self.start = start
        self.end = end
        self.codeword = codeword

    def replace_in(self, s: str) -> str:
        """Replaces the codeword in the string with the tags.

        This method finds all the occurrences of the codeword in
        the string and splits the string into segments by the codeword.
        Then, it alternates the segments with the tags and returns the modified string.

        Args:
            s (str): The string to replace the codeword in.

        Returns:
            str: The string with the codeword replaced by the tags.

        Examples:
            >>> tag = Tag("<b>", "</b>", "**")
            >>> tag.replace_in("This is **bold** text.")
            'This is <b>bold</b> text.'
        """
        indexes = [i for i, _ in enumerate(s) if s.startswith(self.codeword, i)]
        segments = s.split(self.codeword)
        result = segments[0]
        for i in range(1, len(segments)):
            if i % 2 == 0:
                result += self.codeword + segments[i]
            else:
                result += self.start + segments[i] + self.end
        return result


def bold(s: str) -> str:
    """Returns a string with tags <strong>, </strong> instead of the codeword **.

    This function uses the BOLD object, which is an instance of the Tag class,
    to replace the codeword ** in the string with the tags <strong>, </strong>.

    Args:
        s (str): The string to replace the codeword in.

    Returns:
        str: The string with the codeword replaced by the tags.

    Examples:
        >>> bold("This is **bold** text.")
        'This is <strong>bold</strong> text.'
    """
    return BOLD.replace_in(s)


def itallic(s: str) -> str:
    """Returns a string with tags <em>, </em> instead of the codeword *.

    This function uses the ITALLIC object, which is an instance of the Tag class,
    to replace the codeword * in the string with the tags <em>, </em>.

    Args:
        s (str): The string to replace the codeword in.

    Returns:
        str: The string with the codeword replaced by the tags.

    Examples:
        >>> itallic("This is *itallic* text.")
        'This is <em>itallic</em> text.'
    """
    return ITALLIC.replace_in(s)


BOLD = Tag("<strong>", "</strong>", "**")
ITALLIC = Tag("<em>", "</em>", "*")
