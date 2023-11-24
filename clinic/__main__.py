"""Start of program."""
from modules import o_io
from modules import models as m
import menu


m.create_tables(
    m.Patient,m.Doctor,
    m.Appointment,m.Vocation,
    m.Shedule,m.User,
    m.Admin)

indent_contr = o_io.IndentationController()
menu.main(indent_contr,True)
