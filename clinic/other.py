"""Needs to be divided into modules."""
import datetime as dt
from enum import Enum
from modules import o_io, o_matrix,o_number
from modules import wrappers as w
from modules import m_table as t
from modules import models as m


class AccessLevel(Enum):
    """Provides access to
    some tables and their columns."""
    ADMIN = 0
    DOCTOR = 1
    PATIENT = 2
    UNKNOWN = 3


def try_get_command_code(end,indent_contr,start = 1):
    """Tries to get command code which was typed by user.
    If the code isn't in the specified range inclusive 
    the function throws Value Error."""
    command_code = indent_contr.get_input_parameter('Command code',int)
    o_number.check_if_number_is_in_range(command_code,start, \
        end,"Command code")
    return command_code


def get_table_by_name(t_name,full_access=True):
    """Returns one table by its
    name from this list: Admins,
    Appointments, Doctors, Patients,
    Shedules, Users, Vocations."""
    match t_name:
        case "Admins":
            ids = [entry.id for entry in m.Admin.select()]
            table = t.Table( \
                ids,m.Admin,["user"],["user"],True)
        case "Appointments":
            ids = [entry.id for entry in m.Appointment.select()]
            table = t.Table( \
                ids,m.Appointment, \
                ["date","start","real_date","real_start", \
                "real_end","patient","doctor","was_over"], \
                ["date","start","real_date","real_start", \
                "real_end","patient","doctor","was_over"], \
                full_access)
        case "Doctors":
            ids = [entry.id for entry in m.Doctor.select()]
            table = t.Table(ids,m.Doctor, \
                ["passport","date_of_birth","full_name", \
                "place_of_residence","user","shedule", \
                "vocation","cabinet","average_appointment_time"], \
                ["passport","date_of_birth", \
                "full_name","place_of_residence","user","shedule", \
                "vocation","cabinet","average_appointment_time"], \
                full_access)
        case "Patients":
            ids = [entry.id for entry in m.Patient.select()]
            table = t.Table(ids,m.Patient,["passport", \
                "date_of_birth","full_name","place_of_residence", \
                "user"],["passport","date_of_birth","full_name", \
                "place_of_residence","user"], \
                full_access)
        case "Shedules":
            ids = [entry.id for entry in m.Shedule.select()]
            table = t.Table(ids,m.Shedule,["days_in_week", \
                "start","lunch_start","lunch_end","end"], \
                ["days_in_week","start","lunch_start","lunch_end", \
                "end"],full_access)
        case "Users":
            ids = [entry.id for entry in m.User.select()]
            table = t.Table(ids,m.User,["email","password"], \
                ["email","password"],full_access)
        case "Vocations":
            ids = [entry.id for entry in m.Vocation.select()]
            table = t.Table(ids,m.Vocation,["name"],["name"], \
                full_access)
        case _:
            raise Exception( \
                f"Table with name {t_name} doesn't exist.")
    return table


def get_tables_related_to_doctor_account(d_id:int):
    """Returns Doctors, Users, Shedules, Vocations tables
    with entry related to the doctor."""
    doctors = get_table_by_name("Doctors",False)
    doctors.ids = [d_id]
    doctors.fields_names_w = \
        ["full_name","passport","average_appointment_time"]
    u_id = doctors.get_wrapper(d_id,"user").number
    v_id = doctors.get_wrapper(d_id,"vocation").number

    users = get_table_by_name("Users",False)
    users.fields_names_w = ["email","password"]
    users.ids = [u_id]

    shedules = get_shedule(d_id)

    vocations = get_table_by_name("Vocations",False)
    vocations.fields_names_w = []
    vocations.ids = [v_id]

    return [doctors,users,shedules,vocations]


def get_tables_related_to_appointments(*,d_id:int=-1,
                                       p_id:int=-1):
    """Returns Appointments, Doctors, Vocations,
    Users, Patients, Users tables with entries
    related to the doctor or the patient."""
    appointments = get_table_by_name("Appointments",False)
    names = appointments.fields_names_r.copy()
    names.insert(0,"ID")

    if p_id == -1:
        index = names.index("doctor")
        appointments.as_str(t.Mode.FILTER,index, \
            start=str(d_id),end=str(d_id))
        appointments.fields_names_w = \
            ["real_date","real_start","real_end","was_over"]
    else:
        index = names.index("patient")
        appointments.as_str(t.Mode.FILTER,index, \
            start=str(p_id),end=str(p_id))
        appointments.fields_names_w = \
            ["real_date","real_start","real_end"]
    cashed = appointments.cashed
    a_ids = list(map( \
        lambda x: x.number,o_matrix.get_column(0,cashed[1:])))
    appointments.ids = a_ids

    doctors,users,_,vocations = get_doctors_info()

    patients = get_table_by_name("Patients",False)
    patients.fields_names_w = []
    patients.fields_names_r = ["full_name"]

    return [appointments,doctors,vocations,users,patients,users]


def get_shedule(d_id:int):
    """Returns immutable Shedules with shedule of the doctor."""
    doctors = get_table_by_name("Doctors",False)

    s_id = doctors.get_wrapper(d_id,"shedule").number
    shedules = get_table_by_name("Shedules",False)
    shedules.fields_names_w = []
    shedules.ids = [s_id]
    return shedules


def get_first_unmarked_appointment(appointments):
    """Returns the first appointment ID for specified doctor
    which wasn't over."""
    appointments.as_str(t.Mode.SORT,4,reverse=False)
    appointments.as_str(t.Mode.SORT,3,reverse=False)
    appointments.as_str(t.Mode.FILTER,8, \
        start="0",end="0")
    a_id = appointments.cashed[1][0].number

    appointments.as_str()
    return a_id


def get_doctors_info():
    """Returns Doctors, Users, Shedules, Vocations
    tables with entries that match doctors."""
    doctors = get_table_by_name("Doctors",False)
    doctors.fields_names_w = []
    doctors.fields_names_r = ["full_name", \
        "average_appointment_time"]

    shedules = get_table_by_name("Shedules",False)
    shedules.fields_names_w = []
    shedules.fields_names_r = \
        ["start","lunch_start", \
        "lunch_end","end"]

    vocations = get_table_by_name("Vocations",False)
    vocations.fields_names_w = []
    vocations.fields_names_r = ["name"]

    users = get_table_by_name("Users",False)
    users.fields_names_w = []
    users.fields_names_r = ["email"]
    return [doctors,users,shedules,vocations]


def check_time(time,shedules,finished_ids,
               appointments):
    """Returns bool that indicates time is in
    valid time span."""

    intermediate = check_time_base(time,shedules)
    if intermediate is False:
        return False

    max_end = w.Time("0:0:0")
    for _id in finished_ids:
        real_end = appointments.get_wrapper(_id.number,"real_end")
        max_end = max(max_end,real_end)

    return time > max_end


def check_time_base(time,shedules):
    """Returns bool that indicates time is in
    valid time span."""
    shedules.as_str()
    *_,start,l_start,l_end,end = shedules.cashed[1]
    if time < start:
        return False
    if l_start.value is None:
        if time <= end:
            return True
        return False
    if time < l_start:
        return True
    if time <= l_end:
        return False
    if time <= end:
        return True
    return False


def optimize_appointments(appointments,shedules):
    """Takes appointments table and shedules table for
    the particular doctor and tries to
    shift real starts and ends for all appointments
    which have not yet been completed
    and maybe dates so that the spans of appointments
    do not intersect each other and all real start
    times are as close as possible to the expected ones."""

    appointments.as_str()
    dates = o_matrix.get_column(1,appointments.cashed[1:])
    unique_dates = []
    for date in dates:
        if not date.date in \
            list(map(lambda x: x.date,unique_dates)):
            unique_dates.append(date)

    unique_dates.sort()

    for _id in appointments.ids:
        date = appointments.get_wrapper(_id,"date")
        appointments.update_field( \
            _id,"real_date",date.value)

    d_index = 0

    while d_index < len(unique_dates):
        date = unique_dates[d_index]

        finished_ids = get_ids_of_appointments(
            appointments,date)
        unfinished_ids = get_ids_of_appointments(
            appointments,date,True)

        weights = [1,1]

        for _i in range(len(unfinished_ids[2:])):
            weights.append(weights[_i] + weights[_i + 1])

        weights = weights[::-1]

        respond = get_not_intersected_spans([],appointments,
                   unfinished_ids,weights,
                   finished_ids,shedules)
        if respond is None:
            _id = unfinished_ids[-1].number
            real_date = appointments.get_wrapper(_id,"real_date")
            weekday = real_date.date.weekday()
            days_in_week = shedules.cashed[1][1].number
            _d = 8 - days_in_week if weekday + 1 == days_in_week \
                else 1
            real_date.date = real_date.date + dt.timedelta(days=_d)
            real_date.value = str(real_date)
            appointments.update_field(_id,"real_date",real_date.value)
            if not real_date.date in \
                list(map(lambda x: x.date,unique_dates)):
                unique_dates.append(real_date)
            unique_dates.sort()
            d_index = unique_dates.index(date)
        else:
            d_index += 1
            _,spans = respond
            for span,_id in zip(spans,unfinished_ids):
                appointments.update_field( \
                    _id.number,"real_start",span[0].value)
                appointments.update_field( \
                    _id.number,"real_end",span[1].value)


def get_not_intersected_spans(spans,appointments,
      unfinished_ids,weights,
      finished_ids,shedules,
      percision = 250):
    """Returns not intersected spans whish
    are located as close as possible to
    preferred start values."""
    if len(unfinished_ids) == 0:
        return [0,spans]

    _id = unfinished_ids[0]
    start = appointments.get_wrapper(_id.number,"start")
    real_start = appointments.get_wrapper(_id.number,"real_start")
    real_end = appointments.get_wrapper(_id.number,"real_end")
    length,_ = real_end - real_start

    min_deltas_sum = 10**20
    result_spans = None
    for new_delta in range(- w.Time.MAX_SECONDS + 1,
                           w.Time.MAX_SECONDS,
                           percision):
        if new_delta < 0:
            new_delta_t = w.Time.from_seconds(abs(new_delta))
            real_start,was_shifted = start - new_delta_t
        else:
            new_delta_t = w.Time.from_seconds(new_delta)
            real_start,was_shifted = start + new_delta_t
        if was_shifted:
            continue
        real_end,was_shifted = real_start + length
        if was_shifted:
            continue

        if not (check_time(real_start,shedules, \
            finished_ids,appointments) and \
            check_time(real_end,shedules, \
            finished_ids,appointments)):
            continue

        new_span = [real_start,real_end]

        cont_flag = 0
        for span in spans:
            if not are_not_spans_intersected(new_span,span):
                cont_flag = 1
                break
        if cont_flag:
            continue

        c_spans = spans.copy()
        c_spans.append([real_start,real_end])

        respond = get_not_intersected_spans( \
            c_spans,appointments,unfinished_ids[1:], \
            weights[1:],finished_ids,shedules)
        if respond is None:
            continue

        c_sum,c_spans = respond
        c_sum += abs(new_delta) \
            * weights[0]
        if c_sum < min_deltas_sum:
            min_deltas_sum = c_sum
            result_spans = c_spans
    if result_spans is None:
        return None
    return [min_deltas_sum,result_spans]


def are_not_spans_intersected(span1,span2):
    """Checks if spans are not intersected."""
    return (span1[0] > span2[1]) or (span1[1] < span2[0])


def get_ids_of_appointments(appointments,date:w.Date=None,
                            unfinished=False):
    """Returns IDs of unfinished of finished appointments.
    IDs sorted in ascending order."""

    if unfinished:
        appointments.as_str(t.Mode.FILTER,8,start="0", \
            end="0")
    else:
        appointments.as_str(t.Mode.FILTER,8,start="1", \
            end="1")

    if not date is None:
        appointments.as_str(t.Mode.FILTER,3,start=date.value, \
            end=date.value)

    appointments.as_str(t.Mode.SORT,0,reverse=False)

    ids = o_matrix.get_column(0,appointments.cashed[1:])

    appointments.as_str()

    return ids


def get_tables_related_to_patient_account(p_id:int):
    """Returns Patients, Users tables
    with entry related to the patient."""
    patients = get_table_by_name("Patients",False)
    patients.ids = [p_id]
    u_id = patients.get_wrapper(p_id,"user").number

    users = get_table_by_name("Users",False)
    users.ids = [u_id]

    return [patients,users]


def sign_in(users,email,password):
    """Sign in as admin, doctor or
    a patient. If it was succesful
    returns user access level (admin,
    doctor,patient,unknown), id of person in
    corresponded table (Admins,Doctors,Patients)
    and email."""
    users.as_str(t.Mode.FILTER,1,
                    start=email,end=email)
    users.as_str(t.Mode.FILTER,2,
                    start=password,
                    end=password)
    cashed = users.cashed

    if len(cashed) == 1:
        raise ValueError("Incorrect email or password.")
    _id = cashed[1][0].number

    result = get_access_level(_id,users)
    result.append(email)
    return result


def get_access_level(user_id,users):
    """Determines access level by user id.
    Returns level and id of person in the
    corresponded table."""
    a_ids = [entry.id for entry in m.Admin.select()]
    admins = t.Table(a_ids,m.Admin,["user"],[],False)
    admins.as_str(t.Mode.FILTER,1, \
        start=str(user_id),end=str(user_id))
    cashed = admins.cashed

    if len(cashed) == 2:
        return [AccessLevel.ADMIN,
                cashed[1][0].number]

    d_ids = [entry.id for entry in m.Doctor.select()]
    doctors = t.Table(d_ids,m.Doctor,["user"],[],False)
    doctors.as_str(t.Mode.FILTER,1, \
        start=str(user_id),end=str(user_id))
    cashed = doctors.cashed

    if len(cashed) == 2:
        return [AccessLevel.DOCTOR,
                cashed[1][0].number]

    p_ids = [entry.id for entry in m.Patient.select()]
    patients = t.Table(p_ids,m.Patient,["user"],[],False)
    patients.as_str(t.Mode.FILTER,1, \
        start=str(user_id),end=str(user_id))
    cashed = patients.cashed

    if len(cashed) == 2:
        return [AccessLevel.PATIENT,
                cashed[1][0].number]

    users.remove_entry(user_id)

    return [AccessLevel.UNKNOWN]


def sign_up(indent_contr,users,
            email,password):
    """Signs up into account as patient.
    Returns access level, id in the
    Patients table and email."""
    _id = users.add_entry(f"{email},{password}")
    users.remove_entry(_id)

    p_id = add_new_patient(indent_contr,users, \
        email,password)
    return [AccessLevel.PATIENT,p_id,email]


def add_new_patient(indent_contr,users,email,password):
    """Adds new patient. Returns patient id."""
    p_ids = [entry.id for entry in m.Patient.select()]
    patients = t.Table(p_ids,m.Patient,[ \
        "passport","date_of_birth","full_name", \
        "place_of_residence","user"], \
        ["passport","date_of_birth", \
        "full_name","place_of_residence", \
        "user"],True)
    passport = indent_contr. \
        get_input_parameter('Passport (series number)',str)
    date_of_birth = indent_contr. \
        get_input_parameter('Date of birth (dd.mm.yyyy)',str)
    full_name = indent_contr. \
        get_input_parameter('Full name',str)
    place_of_residence = indent_contr. \
        get_input_parameter(
            'Place of residence (country city street ' + \
                'building apartment)',str)

    user_id = str(users.add_entry(f"{email},{password}"))

    patient_id = patients.add_entry( \
        f"{passport},{date_of_birth},{full_name}," + \
        f"{place_of_residence},{user_id}")
    return patient_id


def handle_menu_exist(indent_contr,
                      result_from_previous_menu,
                      print_docs_func=None):
    """Handles exist from menu."""
    if result_from_previous_menu is None:
        raise o_io.StopProgramException
    if result_from_previous_menu == [] \
        and not print_docs_func is None:
        print_docs_func(indent_contr)
