-- Optional SQL to inspect structure. The application uses SQLAlchemy to create tables automatically.
CREATE TABLE patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    contact TEXT,
    address TEXT
);

CREATE TABLE doctor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT,
    contact TEXT
);

CREATE TABLE appointment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date TEXT,
    notes TEXT,
    FOREIGN KEY(patient_id) REFERENCES patient(id),
    FOREIGN KEY(doctor_id) REFERENCES doctor(id)
);
