"""Models of tables in database."""
import peewee as pw
from modules import wrappers as w


PATH_TO_DB = "data.db"
DB = pw.SqliteDatabase(PATH_TO_DB)


class BaseModel(pw.Model):
    """Empty model with specified
    connection to database."""

    class Meta:
        """Connection to database."""
        database = DB


    @classmethod
    def check_values_for_fields(cls,names_values:dict):
        """Checks values for fields. In the case of
        success returns wrappers related to fields.
        Otherwise throws NotValidFormat or ValueError
        exceptions."""
        result = []
        for key,value in names_values.items():
            elem = cls.get_wrapper_by_name(key,value)
            if elem is None:
                raise ValueError("There is no field with such name.")
            result.append(elem)

        return result


    @classmethod
    def get_wrapper_by_name(cls,name,value):
        """Returns wrapper with designated
        name. Passes value when creates wrapper."""
        raise NotImplementedError


    @classmethod
    def get_key_fields_names_and_types(cls):
        """Returns 2D array where to each foreign key
        field match it's name and type."""
        return []


class Person(BaseModel):
    """Model of persons table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Patients"


    passport = pw.CharField(unique=True,max_length=20)
    date_of_birth = pw.CharField(max_length=10)
    full_name = pw.CharField(max_length=50)
    place_of_residence = pw.CharField(max_length=100)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        match name:
            case "passport":
                return w.Passport(value)
            case "date_of_birth":
                return w.Date(value)
            case "full_name":
                return w.FullName(value)
            case "place_of_residence":
                return w.Location(value)


class User(BaseModel):
    """Model of users table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Users"
    email = pw.CharField(unique=True,max_length=30)
    password = pw.CharField(max_length=25)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        match name:
            case "email":
                return w.Email(value)
            case "password":
                return w.CharField(value)


class Patient(Person):
    """Model of patients table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Patients"
    user = pw.ForeignKeyField(User,unique=True)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        result = super().get_wrapper_by_name(name,value)
        match name:
            case "user":
                result = w.IntNumber(value)
        return result


    @classmethod
    def get_key_fields_names_and_types(cls):
        return [["user",User]]


class Shedule(BaseModel):
    """Model of shedules table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Shedules"

    days_in_week = pw.CharField(max_length=1)

    start = pw.CharField(max_length=8)

    lunch_start = pw.CharField(max_length=8,null=True)
    lunch_end = pw.CharField(max_length=8,null=True)

    end = pw.CharField(max_length=8)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        match name:
            case "days_in_week":
                return w.IntNumber(value)
            case "start":
                return w.Time(value)
            case "lunch_start":
                return w.Time(value)
            case "lunch_end":
                return w.Time(value)
            case "end":
                return w.Time(value)


class Vocation(BaseModel):
    """Model of vocations table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Vocations"

    name = pw.CharField(max_length=25)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        match name:
            case "name":
                return w.CharField(value)


class Doctor(Person):
    """Model of doctors table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Doctors"

    user = pw.ForeignKeyField(User,unique=True)
    shedule = pw.ForeignKeyField(Shedule)
    vocation = pw.ForeignKeyField(Vocation)
    cabinet = pw.CharField(max_length=4)
    average_appointment_time = pw.CharField(max_length=8)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        result = super().get_wrapper_by_name(name,value)
        match name:
            case "user":
                result = w.IntNumber(value)
            case "shedule":
                result = w.IntNumber(value)
            case "vocation":
                result = w.IntNumber(value)
            case "cabinet":
                result = w.IntNumber(value)
            case "average_appointment_time":
                result = w.Time(value)
        return result


    @classmethod
    def get_key_fields_names_and_types(cls):
        return [["user",User],
          ["shedule",Shedule],
          ["vocation",Vocation]]


class Appointment(BaseModel):
    """Model of appointments table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Appointments"

    date = pw.CharField(max_length=10)
    start = pw.CharField(max_length=8)

    real_date = pw.CharField(max_length=10)
    real_start = pw.CharField(max_length=8)
    real_end = pw.CharField(max_length=8)

    patient = pw.ForeignKeyField(Patient)
    doctor = pw.ForeignKeyField(Doctor)

    was_over = pw.CharField(max_length=1)

    @classmethod
    def get_wrapper_by_name(cls, name, value):
        match name:
            case "date":
                return w.Date(value)
            case "start":
                return w.Time(value)
            case "real_date":
                return w.Date(value)
            case "real_start":
                return w.Time(value)
            case "real_end":
                return w.Time(value)
            case "patient":
                return w.IntNumber(value)
            case "doctor":
                return w.IntNumber(value)
            case "was_over":
                return w.Bool(value)


    @classmethod
    def get_key_fields_names_and_types(cls):
        return [["patient",Patient],
          ["doctor",Doctor]]


class Admin(BaseModel):
    """Model of admins table."""
    class Meta:
        """Connection,name of table."""
        db_table = "Admins"
    user = pw.ForeignKeyField(User,unique=True)


    @classmethod
    def get_wrapper_by_name(cls, name, value):
        match name:
            case "user":
                return w.IntNumber(value)


    @classmethod
    def get_key_fields_names_and_types(cls):
        return [["user",User]]


def create_tables(*models):
    """Creates tables based on specified models."""
    DB.create_tables(models)
