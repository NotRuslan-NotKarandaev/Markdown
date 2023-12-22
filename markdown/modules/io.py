"""Custom input and output of variables."""
from enum import Enum
from modules import number


class TextBlockType(Enum):
    """Types of text blocks."""
    DEFAULT = 0
    INFO = 1
    INPUT = 2
    ERROR = 3


class ResponseType(Enum):
    """Types of menu response."""
    EXIST = 0
    BACK = 1


class Wrapper:
    """Wrapper over object."""
    def __init__(self,obj,r_type:ResponseType) -> None:
        self.obj = obj
        self.r_type = r_type


class IndentationController:
    """A class that controls the indentations between text blocks.

    This class has an attribute called previous_text_block_type,
    which stores the type of the last text block that was printed.
    It also has several methods that handle the input and output of
    different types of text blocks, such as info, input, error, etc.
    The methods use the previous_text_block_type attribute to determine
    whether to add indentation or separators between the text blocks.
    """

    def __init__(self,previous_text_block_type=TextBlockType.DEFAULT):
        """Initializes the IndentationController object with the given argument.

        Args:
            previous_text_block_type (TextBlockType): The type of the previous text block.
            The default value is TextBlockType.DEFAULT, which means no previous text block.
        """
        self.previous_text_block_type = previous_text_block_type


    def try_add_indentation(self,text_block_type):
        """Adds indentation between text blocks if it is needed.

        This method checks the type of the current text block and the type
        of the previous text block, and decides whether to add a blank line
        or a separator line between them. It also updates the previous_text_block_type
        attribute with the current text block type.

        Args:
            text_block_type (TextBlockType): The type of the current text block.

        Returns:
            None

        Examples:
            >>> controller = IndentationController()
            >>> controller.try_add_indentation(TextBlockType.INFO)
            >>> controller.try_add_indentation(TextBlockType.INPUT)

        """
        if (self.previous_text_block_type in \
            [TextBlockType.INFO,TextBlockType.INPUT,
            TextBlockType.ERROR]) and \
            (text_block_type in [TextBlockType.INFO,
            TextBlockType.INPUT,TextBlockType.DEFAULT]):
            print()
        if text_block_type == TextBlockType.ERROR:
            if self.previous_text_block_type == TextBlockType.ERROR:
                print("----------AND----------")
            else:
                print("-----------+-----------")

        self.previous_text_block_type = text_block_type


    def try_get_command_code(self,end,start = 1):
        """Tries to get the command code that was typed by the user.

        This method calls the get_input_parameter method to get an
        integer input from the user, and then uses the number module
        to check if the input is in the specified range inclusive.
        If the input is valid, it returns the input as the command code.
        If the input is not valid, it raises a ValueError.

        Args:
            end (int): The upper bound of the valid range for the command code.
            start (int): The lower bound of the valid range for the command code. The default value is 1.

        Returns:
            int: The command code that was typed by the user.

        Raises:
            ValueError: If the input is not in the specified range inclusive.

        Examples:
            >>> controller = IndentationController()
            >>> controller.try_get_command_code(5)
            Command code = 3
            3
            >>> controller.try_get_command_code(5)
            Command code = 6
            ValueError: Command code must be in range from 1 to 5 inclusive.
        """
        command_code = self.get_input_parameter('Command code',int)
        number.check_if_number_is_in_range(command_code,start, \
            end,"Command code")
        return command_code


    def get_input_parameter(self,param_name, str_conversion,
                        cancel_word = 'x'):
        """Gets an input parameter from the user and converts it to the desired type.

        This method prints the name of the input parameter, and then prompts the user 
        to type the value of the parameter. It then tries to convert the input to the
        desired type using the str_conversion function. If the conversion is successful,
        it returns the converted parameter. If the conversion fails, it raises a ValueError.
        If the user types the cancel word, it raises a StopProgramException.

        Args:
            param_name (str): The name of the input parameter.
            str_conversion (function): The function that converts the input string to the desired type.
            cancel_word (str): The word that the user can type to cancel the input. The default value is 'x'.

        Returns:
            The converted parameter.

        Raises:
            ValueError: If the input cannot be converted to the desired type.
            StopProgramException: If the user types the cancel word.

        Examples:
            >>> controller = IndentationController()
            >>> controller.get_input_parameter('Name', str)
            Name = Alice
            'Alice'
            >>> controller.get_input_parameter('Age', int)
            Age = 25
            25
            >>> controller.get_input_parameter('Age', int)
            Age = Bob
            ValueError: invalid literal for int() with base 10: 'Bob'
            >>> controller.get_input_parameter('Name', str, cancel_word='q')
            Name = q
            StopProgramException
        """

        self.try_add_indentation(TextBlockType.INPUT)

        input_string = input(f'{param_name} = ')
        if input_string == cancel_word:
            raise StopProgramException

        parameter = str_conversion(input_string)
        return parameter


    def get_input_array(self,array_name,
                        str_conversion,
                        separator = ',',
                        cancel_word = 'x'):
        """Gets an input array from the user and converts its
        elements to the desired type.

        This method prints the name of the input array, and then prompts the user
        to type the values of the elements separated by the separator. It then
        splits the input string by the separator and tries to convert each element
        to the desired type using the str_conversion function. If the conversion is successful,
        it returns the converted elements as an array. If the conversion fails, it raises a
        ValueError. If the user types the cancel word, it raises a StopProgramException.

        Args:
            array_name (str): The name of the input array.
            str_conversion (function): The function that converts the input string to the desired type.
            separator (str): The separator that the user uses to separate the elements.
            The default value is ','.
            cancel_word (str): The word that the user can type to cancel the input. The default value is 'x'.

        Returns:
            list: The converted elements as an array.

        Raises:
            ValueError: If any element cannot be converted to the desired type.
            StopProgramException: If the user types the cancel word.

        Examples:
            >>> controller = IndentationController()
            >>> controller.get_input_array('Numbers', int)
            Numbers:
            1,2,3,4,5
            [1, 2, 3, 4, 5]
            >>> controller.get_input_array('Names', str, separator=';')
            Names:
            Alice;Bob;Charlie
            ['Alice', 'Bob', 'Charlie']
            >>> controller.get_input_array('Numbers', int)
            Numbers:
            1,2,a,4,5
            ValueError: invalid literal for int() with base 10: 'a'
            >>> controller.get_input_array('Names', str, cancel_word='q')
            Names:
            q
            StopProgramException
        """

        self.try_add_indentation(TextBlockType.INPUT)

        print(f'{array_name}:')

        input_string = input()
        if input_string == cancel_word:
            raise StopProgramException

        str_elements = input_string.split(separator)

        array = [str_conversion(elem) \
            for elem in str_elements]

        return array


    def print_variable(self,variable_name,variable_value):
        """Prints the name and the value of a variable.

        This method prints the name and the value of a variable, separated by an equal sign.
        It uses the str function to convert the value to a string.

        Args:
            variable_name (str): The name of the variable.
            variable_value (any): The value of the variable.

        Returns:
            None

        Examples:
            >>> controller = IndentationController()
            >>> controller.print_variable('Name', 'Alice')
            Name = Alice
            >>> controller.print_variable('Age', 25)
            Age = 25
        """
        self.try_add_indentation(TextBlockType.INFO)

        print(f"{variable_name} = {str(variable_value)}")


    def print_array(self,array_name,array):
        """Prints the name and the values of an array.

        This method prints the name of the array, followed by a newline, and then prints the values of the array, separated by spaces. It uses the map and str functions to convert the values to strings.

        Args:
            array_name (str): The name of the array.
            array (list): The values of the array.

        Returns:
            None

        Examples:
            >>> controller = IndentationController()
            >>> controller.print_array('Numbers', [1, 2, 3, 4, 5])
            Numbers:
            1 2 3 4 5
            >>> controller.print_array('Names', ['Alice', 'Bob', 'Charlie'])
            Names:
            Alice Bob Charlie
        """
        self.try_add_indentation(TextBlockType.INFO)
        array_as_str = ' '.join(map(str,array))

        output_str = f'{array_name}:\n{array_as_str}'
        print(output_str)


    def print_exception(self,ex):
        """Prints the exception message.

        This method prints the exception message that is passed as an argument. It uses the str function to convert the exception to a string.

        Args:
            ex (Exception): The exception to print.

        Returns:
            None

        Examples:
            >>> controller = IndentationController()
            >>> controller.print_exception(ValueError('Invalid input'))
            -----------+-----------
            Invalid input
            >>> controller.print_exception(StopProgramException)
            ----------AND----------
            StopProgramException
        """
        self.try_add_indentation(TextBlockType.ERROR)
        print(ex)


    def print_text(self,text,header=None):
        """Prints the text.

        This method prints the text that is passed as an argument.
        If a header is also passed, it prints the header followed by a
        newline before the text. It uses the str function to convert the
        text and the header to strings.

        Args:
            text (str): The text to print.
            header (str): The header to print before the text. The default
            value is None, which means no header.

        Returns:
            None

        Examples:
            >>> controller = IndentationController()
            >>> controller.print_text('Hello, world!')
            Hello, world!
            >>> controller.print_text('This is a header', 'Header')
            Header:
            This is a header
        """
        self.try_add_indentation(TextBlockType.INFO)
        if not header is None:
            print(f"{header}:")
        print(text)


class StopProgramException(Exception):
    """The exception will be thrown when the user decides to stop typing."""

    def __init__(self):
        super().__init__('Program was stopped.')


class BackToPreviousException(Exception):
    """The exception will be thrown when the user decides to come back
    to the previous menu."""

    def __init__(self,message=None,
                 value_to_return=None):
        if message is None:
            super().__init__('You are back to the previous menu.')
        else:
            super().__init__(message)
        self.value_to_return = value_to_return


def loop(is_main=True,cmds_number=0,
         docs=None):
    """Loops a function with the ability
    to stop the loop. There is exception handling.
    You also can specify if this loop is main
    and add function that prints docs of the loop."""
    def wrap(func):
        def loop(indent_contr,code=None,**kwargs):
            if not docs is None:
                docs(indent_contr)
            while True:
                try:
                    if cmds_number != 0:
                        code = indent_contr.try_get_command_code(cmds_number)
                        if code == 1 and (not docs is None):
                            docs(indent_contr)
                            continue
                        result = func(indent_contr,code,**kwargs)
                    else:
                        result = func(indent_contr,**kwargs)
                    if not isinstance(result,Wrapper):
                        continue
                    match result.r_type:
                        case ResponseType.EXIST:
                            raise StopProgramException
                        case ResponseType.BACK:
                            if not docs is None:
                                docs(indent_contr)

                except StopProgramException as ex:
                    if is_main:
                        indent_contr.print_exception(ex)
                    result = Wrapper(None,ResponseType.EXIST)
                    return result
                except BackToPreviousException as ex:
                    indent_contr.print_exception(ex)
                    result = Wrapper(ex.value_to_return,
                                     ResponseType.BACK)
                    return result
                except Exception as ex:
                    indent_contr.print_exception(ex)

        return loop
    return wrap
