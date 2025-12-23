from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Optional

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[Optional()])
    gender = SelectField('Gender', choices=[('', ''), ('Male','Male'), ('Female','Female'), ('Other','Other')], validators=[Optional()])
    contact = StringField('Contact', validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional()])
    parentname = StringField('Parent Name', validators=[DataRequired()])
    parentnumber = StringField('Parent Contact', validators=[Optional()])
    cause = StringField('Cause/Reason for Visit', validators=[Optional()])
    submit = SubmitField('Save')

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    specialty = StringField('Specialty', validators=[Optional()])
    contact = StringField('Contact', validators=[Optional()])
    submit = SubmitField('Save')

class AppointmentForm(FlaskForm):
    patient = SelectField('Patient', coerce=int, validators=[DataRequired()])
    doctor = SelectField('Doctor', coerce=int, validators=[DataRequired()])
    appointment_date = DateTimeField('Appointment Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()], default=None)
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Create')
