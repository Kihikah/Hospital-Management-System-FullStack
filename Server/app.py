import os
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from dotenv import load_dotenv
from models import db, Doctor, Appointment, Medical_Record, Patient, Outpatient, Inpatient, Department

# Load environment variables
load_dotenv()

# Initialize app and config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback-secret")

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
api = Api(app)

#---------------------- PATIENT ROUTES ----------------------
class HomeResource(Resource):
    def get(self):
        return make_response(jsonify({"message": "Welcome to the Hospital Management System API!"}), 200)

class Patient_List(Resource):
    def get(self):
        patients = [patient.to_dict() for patient in Patient.query.all()]
        return make_response(jsonify(patients), 200)

    def post(self):
        data = request.get_json()
        patient_type = data.get('type')

        if patient_type == 'inpatient':
            new_patient = Inpatient(
                name=data['name'], age=data['age'], gender=data['gender'], type='inpatient',
                admission_date=data['admission_date'], ward_number=data['ward_number']
            )
        elif patient_type == 'outpatient':
            new_patient = Outpatient(
                name=data['name'], age=data['age'], gender=data['gender'], type='outpatient',
                last_visit_date=data['last_visit_date']
            )
        else:
            new_patient = Patient(
                name=data['name'], age=data['age'], gender=data['gender'], type='patient'
            )

        db.session.add(new_patient)
        db.session.commit()
        return make_response(new_patient.to_dict(), 201)

class Patient_By_ID(Resource):
    def get(self, id):
        patient = Patient.query.get(id)
        if not patient:
            return make_response({"error": "Patient not found"}, 404)
        return make_response(patient.to_dict(), 200)

    def delete(self, id):
        patient = Patient.query.get(id)
        if not patient:
            return make_response({"error": "Patient not found"}, 404)
        db.session.delete(patient)
        db.session.commit()
        return make_response({"message": "Patient deleted"}, 204)

class PatientMedicalRecords(Resource):
    def get(self, id):
        patient = Patient.query.get(id)
        if not patient:
            return make_response({"error": "Patient not found"}, 404)
        return make_response([record.to_dict() for record in patient.medical_records], 200)

#---------------------- APPOINTMENT ROUTES ----------------------
class AppointmentList(Resource):
    def get(self):
        appointments = Appointment.query.all()
        return jsonify([a.to_dict() for a in appointments])

    def post(self):
        data = request.get_json()
        new_appt = Appointment(**data)
        db.session.add(new_appt)
        db.session.commit()
        return jsonify(new_appt.to_dict()), 201

class AppointmentByID(Resource):
    def get(self, id):
        appt = Appointment.query.get(id)
        return jsonify(appt.to_dict()) if appt else (jsonify({"error": "Not found"}), 404)

    def patch(self, id):
        appt = Appointment.query.get(id)
        if not appt:
            return jsonify({"error": "Not found"}), 404
        for key, value in request.get_json().items():
            setattr(appt, key, value)
        db.session.commit()
        return jsonify(appt.to_dict())

    def delete(self, id):
        appt = Appointment.query.get(id)
        if not appt:
            return jsonify({"error": "Not found"}), 404
        db.session.delete(appt)
        db.session.commit()
        return jsonify({"message": "Deleted"})

#---------------------- DOCTOR ROUTES ----------------------
class DoctorList(Resource):
    def get(self):
        return jsonify([d.to_dict() for d in Doctor.query.all()])

    def post(self):
        data = request.get_json()
        new_doc = Doctor(**data)
        db.session.add(new_doc)
        db.session.commit()
        return jsonify(new_doc.to_dict()), 201

class DoctorByID(Resource):
    def get(self, id):
        doctor = Doctor.query.get(id)
        return jsonify(doctor.to_dict()) if doctor else (jsonify({"error": "Not found"}), 404)

    def patch(self, id):
        doc = Doctor.query.get(id)
        if not doc:
            return jsonify({"error": "Not found"}), 404
        for k, v in request.get_json().items():
            setattr(doc, k, v)
        db.session.commit()
        return jsonify(doc.to_dict())

    def delete(self, id):
        doc = Doctor.query.get(id)
        if not doc:
            return jsonify({"error": "Not found"}), 404
        db.session.delete(doc)
        db.session.commit()
        return jsonify({"message": "Deleted"})

#---------------------- MEDICAL RECORDS ----------------------
class MedicalRecords(Resource):
    def get(self):
        return jsonify([r.to_dict() for r in Medical_Record.query.all()])

    def post(self):
        data = request.get_json()
        record = Medical_Record(**data)
        db.session.add(record)
        db.session.commit()
        return make_response(record.to_dict(), 201)

class MedicalRecordByID(Resource):
    def get(self, id):
        r = Medical_Record.query.get(id)
        return (make_response(r.to_dict(), 200) if r else make_response({"error": "Not found"}, 404))

    def patch(self, id):
        r = Medical_Record.query.get(id)
        if not r:
            return make_response({"error": "Not found"}, 404)
        for key, value in request.get_json().items():
            setattr(r, key, value)
        db.session.commit()
        return make_response(r.to_dict(), 200)

    def delete(self, id):
        r = Medical_Record.query.get(id)
        if not r:
            return make_response({"error": "Not found"}, 404)
        db.session.delete(r)
        db.session.commit()
        return make_response({"message": "Deleted"}, 204)

#---------------------- DEPARTMENTS ----------------------
class DepartmentList(Resource):
    def get(self):
        return jsonify([d.to_dict() for d in Department.query.all()])

    def post(self):
        data = request.get_json()
        dept = Department(**data)
        db.session.add(dept)
        db.session.commit()
        return make_response(dept.to_dict(), 201)

class DepartmentByID(Resource):
    def get(self, id):
        dept = Department.query.get(id)
        return make_response(dept.to_dict(), 200) if dept else make_response({"error": "Not found"}, 404)

    def patch(self, id):
        dept = Department.query.get(id)
        if not dept:
            return make_response({"error": "Not found"}, 404)
        for k, v in request.get_json().items():
            setattr(dept, k, v)
        db.session.commit()
        return make_response(dept.to_dict(), 200)

    def delete(self, id):
        dept = Department.query.get(id)
        if not dept:
            return make_response({"error": "Not found"}, 404)
        db.session.delete(dept)
        db.session.commit()
        return make_response({"message": "Deleted"}, 204)

# Register RESTful resources
api.add_resource(HomeResource, '/')
api.add_resource(Patient_List, '/patients/')
api.add_resource(Patient_By_ID, '/patients/<int:id>')
api.add_resource(PatientMedicalRecords, '/patients/<int:id>/records')
api.add_resource(MedicalRecords, '/records/')
api.add_resource(MedicalRecordByID, '/records/<int:id>')
api.add_resource(DepartmentList, '/departments/')
api.add_resource(DepartmentByID, '/departments/<int:id>')
api.add_resource(AppointmentList, '/appointments/')
api.add_resource(AppointmentByID, '/appointments/<int:id>')
api.add_resource(DoctorList, '/doctors/')
api.add_resource(DoctorByID, '/doctors/<int:id>')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5555)
