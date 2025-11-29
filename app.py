from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import PatientForm, DoctorForm, AppointmentForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# NOTE: Replace this in production with a secure random key
app.config['SECRET_KEY'] = 'change-me-to-a-secret-key'

db = SQLAlchemy(app)

# Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    contact = db.Column(db.String(50))
    address = db.Column(db.String(250))
    parentname=db.column(db.string,nullabel=False)
    parentnumber=db.column(db.int(100))


    def __repr__(self):
        return f"<Patient {self.name}>"

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120))
    contact = db.Column(db.String(50))

    def __repr__(self):
        return f"<Doctor {self.name}>"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.String(50))
    notes = db.Column(db.String(500))

    patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))

    def __repr__(self):
        return f"<Appointment {self.id} - P{self.patient_id} D{self.doctor_id}>"

# Create tables before first request
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    patients_count = Patient.query.count()
    doctors_count = Doctor.query.count()
    appointments_count = Appointment.query.count()
    return render_template('index.html', patients_count=patients_count, doctors_count=doctors_count, appointments_count=appointments_count)

# Patients
@app.route('/patients')
def patients_list():
    patients = Patient.query.order_by(Patient.name).all()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET','POST'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        p = Patient(name=form.name.data, age=form.age.data, gender=form.gender.data, contact=form.contact.data, address=form.address.data)
        db.session.add(p)
        db.session.commit()
        flash('Patient added successfully', 'success')
        return redirect(url_for('patients_list'))
    return render_template('add_patient.html', form=form, edit=False)

@app.route('/patients/edit/<int:patient_id>', methods=['GET','POST'])
def edit_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash('Patient updated', 'success')
        return redirect(url_for('patients_list'))
    return render_template('add_patient.html', form=form, edit=True)

@app.route('/patients/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    p = Patient.query.get_or_404(patient_id)
    db.session.delete(p)
    db.session.commit()
    flash('Patient deleted', 'warning')
    return redirect(url_for('patients_list'))

# Doctors
@app.route('/doctors')
def doctors_list():
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET','POST'])
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        d = Doctor(name=form.name.data, specialty=form.specialty.data, contact=form.contact.data)
        db.session.add(d)
        db.session.commit()
        flash('Doctor added', 'success')
        return redirect(url_for('doctors_list'))
    return render_template('add_doctor.html', form=form, edit=False)

@app.route('/doctors/edit/<int:doctor_id>', methods=['GET','POST'])
def edit_doctor(doctor_id):
    d = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(obj=d)
    if form.validate_on_submit():
        form.populate_obj(d)
        db.session.commit()
        flash('Doctor updated', 'success')
        return redirect(url_for('doctors_list'))
    return render_template('add_doctor.html', form=form, edit=True)

@app.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    d = Doctor.query.get_or_404(doctor_id)
    db.session.delete(d)
    db.session.commit()
    flash('Doctor deleted', 'warning')
    return redirect(url_for('doctors_list'))

# Appointments
@app.route('/appointments')
def appointments_list():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET','POST'])
def add_appointment():
    form = AppointmentForm()
    # populate choices
    form.patient.choices = [(p.id, p.name) for p in Patient.query.order_by(Patient.name).all()]
    form.doctor.choices = [(d.id, d.name + ' (' + (d.specialty or 'General') + ')') for d in Doctor.query.order_by(Doctor.name).all()]
    if form.validate_on_submit():
        ap = Appointment(patient_id=form.patient.data, doctor_id=form.doctor.data, appointment_date=form.appointment_date.data.strftime('%Y-%m-%d %H:%M'), notes=form.notes.data)
        db.session.add(ap)
        db.session.commit()
        flash('Appointment created', 'success')
        return redirect(url_for('appointments_list'))
    return render_template('add_appointment.html', form=form)

@app.route('/appointments/delete/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    a = Appointment.query.get_or_404(appointment_id)
    db.session.delete(a)
    db.session.commit()
    flash('Appointment removed', 'warning')
    return redirect(url_for('appointments_list'))

@app.route('/appointments/edit/<int:appointment_id>', methods=['GET','POST'])
def edit_appointment(appointment_id):
    a = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=a)
    # populate choices
    form.patient.choices = [(p.id, p.name) for p in Patient.query.order_by(Patient.name).all()]
    form.doctor.choices = [(d.id, d.name + ' (' + (d.specialty or 'General') + ')') for d in Doctor.query.order_by(Doctor.name).all()]
    if form.validate_on_submit():
        a.patient_id = form.patient.data
        a.doctor_id = form.doctor.data
        a.appointment_date = form.appointment_date.data.strftime('%Y-%m-%d %H:%M')
        a.notes = form.notes.data
        db.session.commit()
        flash('Appointment updated', 'success')
        return redirect(url_for('appointments_list'))
    # Pre-fill the date field
    form.appointment_date.data = datetime.strptime(a.appointment_date, '%Y-%m-%d %H:%M')
    return render_template('add_appointment.html', form=form, edit=True)    


if __name__ == '__main__':
    app.run(debug=True)
