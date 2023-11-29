"""Shows commands for some menu."""


def print_startup_cmds(indent_contr):
    """Shows startup commands."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - sign in;\n' + \
        '2 - sign up as a patient.')


def print_admin_cmds(indent_contr):
    """Shows commands for administrator."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - select table;\n' + \
        '4 - select tables for join.')


def print_cmds_for_work_with_table(indent_contr):
    """Shows commands for work with the table
    for administrator."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - add entry;\n' + \
        '4 - remove entry;\n' + \
        '5 - edit entry;\n' + \
        '6 - print original table;\n' + \
        '7 - print cashed table;\n' + \
        '8 - search entries by column;\n' + \
        '9 - sort entries by column;\n' + \
        '10 - filter entries by column.')


def print_cmds_for_work_with_joined_tables(indent_contr):
    """Shows commands for work with the joined tables
    for administrator."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - print original table;\n' + \
        '4 - print cashed table;\n' + \
        '5 - search entries by column;\n' + \
        '6 - sort entries by column;\n' + \
        '7 - filter entries by column.')


def print_cmds_for_doctor(indent_contr):
    """Shows commands for doctor."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - my account;\n' + \
        '4 - my appointments.')


def print_cmds_for_doctor_appointments(indent_contr):
    """Shows commands for doctor's appointments."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - show appointments;\n' + \
        '4 - set end time for the first unmarked appointment;\n' + \
        '5 - remove the first unmarked appointment.')


def print_cmds_for_patient_appointments(indent_contr):
    """Shows commands for patient's appointments."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - show my appointments;\n' + \
        '4 - remove appointment.')


def print_account_cmds(indent_contr):
    """Shows commands for account of
    doctor or patient."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - show personal data;\n' + \
        '4 - change property.')


def print_cmds_for_patient(indent_contr):
    """Shows commands for patient."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - my account;\n' + \
        '4 - doctors;\n' + \
        '5 - my appointments;\n' + \
        '6 - remove account.')


def print_cmds_for_make_appointment(indent_contr):
    """Shows commands for make an appointment."""
    indent_contr. \
        print_text('Press "x" to stop program.\n\n' + \
        "Types of commands and their codes:\n" + \
        '1 - help;\n' + \
        '2 - back to the previous menu;\n' + \
        '3 - show all doctors;\n' + \
        '4 - schedule an appointment.')
