"""Some menu."""
import other
from modules import o_io, o_matrix
from modules import wrappers as w
from modules import m_table as t
from modules import models as m
import menu_cmds as cmds


@o_io.loop
def main(indent_contr,is_main):
    """Provides such functions
    as sign in, sign up, go to
    some mode (admin,doctor,patient)."""
    cmds.print_startup_cmds(indent_contr)
    result = startup(indent_contr,False)

    other.handle_menu_exist(indent_contr,result)
    access_lvl,_id = result

    match access_lvl:
        case other.AccessLevel.ADMIN:
            indent_contr.print_text( \
                "You was signed in as an administrator.")
            cmds.print_admin_cmds(indent_contr)
            result = admin_mode(indent_contr,False,_id=_id)
        case other.AccessLevel.DOCTOR:
            indent_contr.print_text( \
                "You was signed in as a doctor.")
            cmds.print_cmds_for_doctor(indent_contr)
            result = doctor_mode(indent_contr,False,_id=_id)
        case other.AccessLevel.PATIENT:
            indent_contr.print_text( \
                "You was signed in as a patient.")
            cmds.print_cmds_for_patient(indent_contr)
            result = patient_mode(indent_contr,False,_id=_id)

    other.handle_menu_exist(indent_contr,result)


@o_io.loop
def startup(indent_contr,is_main):
    """Tries to sign in or sign up.
    If it was succesful returns user
    access level (admin, doctor, patient, unknown),
    id of person in corresponded table
    (Admins, Doctors, Patients)."""
    code = other.try_get_command_code(2,indent_contr)
    email = indent_contr. \
        get_input_parameter('Email',str)
    password = indent_contr. \
        get_input_parameter('Password',str)

    u_ids = [entry.id for entry in m.User.select()]
    users = t.Table(u_ids,m.User,["email","password"],
                    ["email","password"],True)

    if code == 1:
        result = other.sign_in( \
            users,email,password)
        if result[0] == other.AccessLevel.UNKNOWN:
            raise Exception( \
                "Can't find any persons related with" + \
                " this user. Try to sign up with this" + \
                " email and password.")
        raise o_io.BackToPreviousException( \
            "You was successfully signed in.\n" + \
            f'Your email: "{result[2]}".',result[:-1])
    result = other.sign_up(indent_contr,users,
                        email,password)
    raise o_io.BackToPreviousException( \
        "You was successfully sigined up.\n" + \
        f'Your email: "{result[2]}".',result[:-1])


@o_io.loop
def admin_mode(indent_contr,is_main,*,_id):
    """Start menu for administrator."""
    code = other.try_get_command_code(4,indent_contr)
    match code:
        case 1:
            cmds.print_admin_cmds(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in statup menu.")
        case 3:
            indent_contr.print_text( \
                "Admins, Appointments, Doctors, Patients, " + \
                "Shedules, Users, Vocations", \
                "Select name of one of the tables")
            t_name = indent_contr.get_input_parameter( \
                "Selected table name",str)
            table = other.get_table_by_name(t_name)

            cmds.print_cmds_for_work_with_table(indent_contr)
            result = work_with_table(indent_contr,False, \
                table=table,t_name=t_name)

            other.handle_menu_exist(indent_contr,result,
                cmds.print_admin_cmds)
        case 4:
            indent_contr.print_text( \
                "Admins, Appointments, Doctors, Patients, " + \
                "Shedules, Users, Vocations", \
                "Select names of two or more tables")
            t_names = indent_contr.get_input_array( \
                "Selected tables names " + \
                "(separated by commas without spaces)",str)
            tables = []
            for t_name in t_names:
                tables.append(other.get_table_by_name(t_name))
            joined = tables[0].join_with(*tables[1:])
            cmds.print_cmds_for_work_with_joined_tables(indent_contr)
            result = work_with_joined_tables(indent_contr, \
                False,joined=joined)
            other.handle_menu_exist(indent_contr,result,
                cmds.print_admin_cmds)


@o_io.loop
def work_with_table(indent_contr,is_main,*,
                    table,t_name):
    """Menu for work with table."""
    code = other.try_get_command_code(10,indent_contr)

    cols = ["ID"]
    cols.extend(table.fields_names_r)

    match code:
        case 1:
            cmds.print_cmds_for_work_with_table(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in admin mode menu.")
        case 3:
            str_entry = indent_contr.get_input_parameter( \
                "Entry (values separated by " + \
                "commas without spaces)",str)
            table.add_entry(str_entry)
        case 4:
            _id = indent_contr.get_input_parameter( \
                "ID of entry",int)
            table.remove_entry(_id)
        case 5:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            _id = indent_contr.get_input_parameter( \
                "Entry's ID",int)
            value = indent_contr.get_input_parameter( \
                "New value",str)
            table.update_field(_id,c_name,value)
        case 6:
            indent_contr.print_text( \
                table.as_str(), \
                f"Original {t_name}")
        case 7:
            indent_contr.print_text( \
                table.as_str( \
                mode=t.Mode.CASHED), \
                f"Cashed {t_name}")
        case 8:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            c_index = cols.index(c_name)

            expr = indent_contr.get_input_parameter( \
                "Regular expression",str)

            indent_contr.print_text( \
                table.as_str( \
                mode=t.Mode.SEARCH, \
                field_index=c_index, \
                regular_expression=expr), \
                f"Searched {t_name}")
        case 9:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            c_index = cols.index(c_name)

            is_reverse = bool(indent_contr.get_input_parameter( \
                "Is reversed (0 or 1)",int))

            indent_contr.print_text( \
                table.as_str( \
                mode=t.Mode.SORT, \
                field_index=c_index, \
                reverse=is_reverse), \
                f"Sorted {t_name}")
        case 10:
            c_name = indent_contr.get_input_parameter( \
                "Column name",str)
            c_index = cols.index(c_name)

            start = indent_contr.get_input_parameter( \
                "Start value",str)
            end = indent_contr.get_input_parameter( \
                "End value",str)

            indent_contr.print_text( \
                table.as_str( \
                mode=t.Mode.FILTER, \
                field_index=c_index, \
                start=start,end=end), \
                f"Filtered {t_name}")


@o_io.loop
def work_with_joined_tables(indent_contr,is_main,*,joined):
    """Menu for wotk with joined tables."""
    code = other.try_get_command_code(7,indent_contr)
    t_name = "joined tables"
    match code:
        case 1:
            cmds.print_cmds_for_work_with_joined_tables(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in admin mode menu.")
        case 3:
            indent_contr.print_text( \
                joined.as_str(), \
                f"Original {t_name}")
        case 4:
            indent_contr.print_text( \
                joined.as_str( \
                mode=t.Mode.CASHED), \
                f"Cashed {t_name}")
        case 5:
            c_index = indent_contr.get_input_parameter( \
                "Column index",int)

            expr = indent_contr.get_input_parameter( \
                "Regular expression",str)

            indent_contr.print_text( \
                joined.as_str( \
                mode=t.Mode.SEARCH, \
                field_index=c_index, \
                regular_expression=expr), \
                f"Searched {t_name}")
        case 6:
            c_index = indent_contr.get_input_parameter( \
                "Column index",int)

            is_reverse = bool(indent_contr.get_input_parameter( \
                "Is reversed (0 or 1)",int))

            indent_contr.print_text( \
                joined.as_str( \
                mode=t.Mode.SORT, \
                field_index=c_index, \
                reverse=is_reverse), \
                f"Sorted {t_name}")
        case 7:
            c_index = indent_contr.get_input_parameter( \
                "Column index",int)

            start = indent_contr.get_input_parameter( \
                "Start value",str)
            end = indent_contr.get_input_parameter( \
                "End value",str)

            indent_contr.print_text( \
                joined.as_str( \
                mode=t.Mode.FILTER, \
                field_index=c_index, \
                start=start,end=end), \
                f"Filtered {t_name}")


@o_io.loop
def doctor_mode(indent_contr,is_main,*,_id):
    """Menu for doctor."""
    code = other.try_get_command_code(4,indent_contr)
    match code:
        case 1:
            cmds.print_cmds_for_doctor(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in statup menu.")
        case 3:
            cmds.print_account_cmds(indent_contr)

            tables = \
                other.get_tables_related_to_doctor_account(_id)

            result = account_menu(indent_contr,False, \
                tables=tables,is_doctor=True)

            other.handle_menu_exist(indent_contr,result,
                cmds.print_cmds_for_doctor)
        case 4:
            cmds.print_cmds_for_doctor_appointments(indent_contr)
            tables = \
                other.get_tables_related_to_appointments(d_id=_id)
            result = appointments_for_doctor(indent_contr,False, \
                tables=tables)
            other.handle_menu_exist(indent_contr,result,
                cmds.print_cmds_for_doctor)


@o_io.loop
def account_menu(indent_contr,is_main,*,tables,
                 is_doctor:bool):
    "Account menu for patient or doctor."
    code = other.try_get_command_code(4,indent_contr)
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 1:
            cmds.print_account_cmds(indent_contr)
        case 2:
            if is_doctor:
                raise o_io.BackToPreviousException( \
                    "You are now in doctor menu.")
            raise o_io.BackToPreviousException( \
                "You are now in patient menu.")
        case 3:
            indent_contr.print_text( \
                joined.as_str(),"Your account")
        case 4:
            p_name = indent_contr.get_input_parameter( \
                "Property name",str)
            value = indent_contr.get_input_parameter( \
                "New value",str)
            for table in tables:
                if p_name in table.fields_names_r:
                    _id = table.ids[0]
                    table.update_field(_id,p_name, \
                        value)
                    break


@o_io.loop
def appointments_for_doctor(indent_contr,is_main,*,tables):
    "Appointments for doctor."
    code = other.try_get_command_code(5,indent_contr)
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 1:
            cmds.print_cmds_for_doctor_appointments(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in doctor menu.")
        case 3:
            joined.as_str(t.Mode.SORT,4,reverse=False)
            joined.as_str(t.Mode.SORT,3,reverse=False)
            joined.as_str(t.Mode.SORT,6,reverse=True)
            indent_contr.print_text( \
                joined.as_str(t.Mode.CASHED), \
                "Your appointments")
        case 4:
            appointments = tables[0]

            a_id = other.get_first_unmarked_appointment( \
                appointments)

            end = indent_contr.get_input_parameter( \
                "End time",w.Time)

            _st = appointments.get_wrapper(a_id,"start")

            if _st >= end:
                raise ValueError("End time before start time.")

            appointments.update_field(a_id,"real_end",end.value)
            appointments.update_field(a_id,"was_over","1")

            d_id = appointments.get_wrapper(a_id,"doctor").number
            shedules = other.get_shedule(d_id)

            other.optimize_appointments(appointments,shedules)
        case 5:
            appointments = tables[0]

            a_id = other.get_first_unmarked_appointment( \
                appointments)

            d_id = appointments.get_wrapper(a_id,"doctor").number
            shedules = other.get_shedule(d_id)

            appointments.full_access = True
            appointments.remove_entry(a_id)
            appointments.full_access = False

            other.optimize_appointments(appointments,shedules)


@o_io.loop
def patient_mode(indent_contr,is_main,*,_id:int):
    """Menu for doctor."""
    code = other.try_get_command_code(6,indent_contr)
    match code:
        case 1:
            cmds.print_cmds_for_patient(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in statup menu.")
        case 3:
            cmds.print_account_cmds(indent_contr)

            tables = \
                other.get_tables_related_to_patient_account(_id)

            result = account_menu(indent_contr,False, \
                tables=tables,is_doctor=False)

            other.handle_menu_exist(indent_contr,result,
                cmds.print_cmds_for_patient)
        case 4:
            cmds.print_cmds_for_make_appointment(indent_contr)

            tables = other.get_doctors_info()

            result = make_appointment(indent_contr,False, \
                p_id=_id,tables=tables)

            other.handle_menu_exist(indent_contr,result,
                cmds.print_cmds_for_patient)
        case 5:
            cmds.print_cmds_for_patient_appointments(indent_contr)
            tables = \
                other.get_tables_related_to_appointments(p_id=_id)

            result = appointments_for_patient(indent_contr,False, \
                tables=tables)
            other.handle_menu_exist(indent_contr,result,
                cmds.print_cmds_for_patient)
        case 6:
            appointments,*_ = \
                other.get_tables_related_to_appointments(p_id=_id)
            appointments.full_access = True
            appointments.as_str()

            a_ids = list(map(lambda x: x.number, \
                o_matrix.get_column(0,appointments.cashed[1:])))
            d_ids = list(map(lambda x: x.number, \
                o_matrix.get_column(7,appointments.cashed[1:])))

            patients,users = other.get_tables_related_to_patient_account(_id)
            patients.full_access = True
            users.full_access = True

            patients.remove_entry(_id)
            users.remove_entry(users.ids[0])

            for a_id in a_ids:
                appointments.remove_entry(a_id)

            for d_id in d_ids:
                doctor_appointments,*_ = \
                    other.get_tables_related_to_appointments(d_id=d_id)
                shedules = other.get_shedule(d_id)
                other.optimize_appointments(
                    doctor_appointments,shedules)

            raise o_io.BackToPreviousException( \
                "You are now in statup menu.")


@o_io.loop
def appointments_for_patient(indent_contr,is_main,*,tables):
    "Appointments for patient."
    code = other.try_get_command_code(4,indent_contr)
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 1:
            cmds.print_cmds_for_patient_appointments(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in patient menu.")
        case 3:
            joined.as_str(t.Mode.SORT,4,reverse=False)
            joined.as_str(t.Mode.SORT,3,reverse=False)
            joined.as_str(t.Mode.SORT,6,reverse=True)
            indent_contr.print_text( \
                joined.as_str(t.Mode.CASHED), \
                "Your appointments")
        case 4:
            appointments = tables[0]

            a_id = indent_contr.get_input_parameter( \
                "Appointment's ID",int)

            was_over = appointments.get_wrapper(a_id,"was_over").number
            if was_over:
                raise Exception( \
                    "You can't remove this. The appointment was over.")

            d_id = appointments.get_wrapper(a_id,"doctor").number
            shedules = other.get_shedule(d_id)

            appointments.full_access = True
            appointments.remove_entry(a_id)
            appointments.full_access = False

            doctor_appointments,*_ = \
                other.get_tables_related_to_appointments(d_id=d_id)

            other.optimize_appointments(doctor_appointments,shedules)


@o_io.loop
def make_appointment(indent_contr,is_main,*,p_id:int,tables):
    "Make appointments for patient."
    code = other.try_get_command_code(4,indent_contr)
    joined = tables[0].join_with(*tables[1:])
    match code:
        case 1:
            cmds.print_cmds_for_make_appointment(indent_contr)
        case 2:
            raise o_io.BackToPreviousException( \
                "You are now in patient menu.")
        case 3:
            indent_contr.print_text( \
                joined.as_str(t.Mode.SORT,8,reverse=False), \
                "Doctors")
        case 4:
            d_id = indent_contr.get_input_parameter( \
                "Doctor's ID",int)
            date = indent_contr.get_input_parameter( \
                "Appointment's date",w.Date)
            time = indent_contr.get_input_parameter( \
                "Appointment's time",w.Time)

            appointments,*_ = \
                other.get_tables_related_to_appointments(d_id=d_id)

            finished_ids = \
                other.get_ids_of_appointments(appointments,date)

            shedules = other.get_shedule(d_id)
            if other.check_time( \
                time,shedules,finished_ids, \
                appointments) is False:
                raise ValueError("This time is busy.")

            finished_ids = \
                other.get_ids_of_appointments(appointments)

            max_date = w.Date("1.1.1")
            for finished_id in finished_ids:
                max_date = max( \
                    appointments.get_wrapper(finished_id.number,"real_date"), \
                    max_date)
            if max_date > date:
                raise Exception("This date has already passed.")


            shedules.as_str()
            days_in_week = shedules.cashed[1][1].number
            weekday = date.date.weekday()

            if weekday >= days_in_week:
                raise Exception( \
                    f"This doctor works only {days_in_week} days in week.")

            doctors = tables[0]
            average = doctors.get_wrapper( \
                d_id,"average_appointment_time")

            real_end,_ = time + average

            appointments = other.get_table_by_name("Appointments")
            appointments.add_entry( \
                date.value + "," + time.value + "," + date.value + \
                "," + time.value + "," + real_end.value + "," + \
                str(p_id) + "," + str(d_id) + ",0")

            other.optimize_appointments(appointments,shedules)
