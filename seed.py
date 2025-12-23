# optional seed data to populate DB quickly
from app import app, db, Patient, Doctor

def seed():
    with app.app_context():
        db.create_all()
        if not Patient.query.first():
            p1 = Patient(name='John Doe', age=30, gender='Male', contact='9999999999', address='123 Street', parentname='Mary Doe', parentnumber='9999999998', cause='General Checkup')
            p2 = Patient(name='Jane Smith', age=25, gender='Female', contact='8888888888', address='456 Avenue', parentname='Robert Smith', parentnumber='8888888887', cause='Flu Symptoms')
            db.session.add_all([p1,p2])
        if not Doctor.query.first():
            d1 = Doctor(name='Dr. Alice', specialty='Cardiology', contact='7777777777')
            d2 = Doctor(name='Dr. Bob', specialty='Orthopedics', contact='6666666666')
            db.session.add_all([d1,d2])
        db.session.commit()
        print('Seeded sample data')

if __name__ == '__main__':
    seed()
