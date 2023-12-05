"""Some menus."""
from modules import io,markdown
import menus_cmds as cmds


@io.loop(cmds_number=2,docs=cmds.print_main_cmds)
def main(indent_contr:io.IndentationController,code):
    """Menu where strings are formatted."""
    match code:
        case 2:
            string = indent_contr.get_input_parameter("Unformatted string",str)
            string = markdown.replace_with_tags(string, \
                [markdown.BOLD,markdown.ITALLIC])
            indent_contr.print_variable("Formatted string",string)
