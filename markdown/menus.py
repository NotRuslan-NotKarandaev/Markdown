"""Some menus."""
import markdown as md1
from modules import markdown as md2
from modules import io
import menus_cmds as cmds



@io.loop(cmds_number=3,docs=cmds.print_main_cmds)
def main(indent_contr:io.IndentationController,code):
    """Menu where strings are formatted."""
    match code:
        case 2:
            string = indent_contr.get_input_parameter("Unformatted string",str)
            string = md1.markdown(string)
            indent_contr.print_variable("Formatted string",string)
        case 3:
            string = indent_contr.get_input_parameter("Unformatted string",str)
            string = md2.replace_with_tags(string, \
                [md2.BOLD,md2.ITALLIC])
            indent_contr.print_variable("Formatted string",string)
