"""Some menus."""
from modules import markdown as md
from modules import io
import menus_cmds as cmds



@io.loop(cmds_number=3,docs=cmds.print_main_cmds)
def main(indent_contr:io.IndentationController,code):
    """Menu where strings are formatted.

    This function is a loop that takes an input code from the user and performs different
    formatting operations on a string, depending on the code. The loop is controlled by the
    `io` module, which also handles the input and output of the parameters and variables.
    The formatting operations are defined by the `markdown` module, which applies bold or itallic tags to the string.

    Args:
        indent_contr (io.IndentationController): An object that controls the indentation 
        level and the input and output methods.
        code (int): A code that indicates the formatting operation to be performed.
        The valid codes are 1 and 2 and 3.

    Returns:
        None

    Raises:
        ValueError: If the code is not 1 or 2 or 3.

    Examples:
        >>> indent_contr = io.IndentationController()
        >>> main(indent_contr,None)
        Command code = 1
        Enter Unformatted string: Hello world
        Formatted string: **Hello world**
        >>> main(indent_contr,None)
        Command code = 2
        Enter Unformatted string: Hello world
        Formatted string: *Hello world*
        >>> main(indent_contr,None)
        Command code = 5
        ValueError: Invalid code
    """
    match code:
        case 2:
            string = indent_contr.get_input_parameter("Unformatted string",str)
            string = md.bold(string)
            indent_contr.print_variable("Formatted string",string)
        case 3:
            string = indent_contr.get_input_parameter("Unformatted string",str)
            string = md.itallic(string)
            indent_contr.print_variable("Formatted string",string)
