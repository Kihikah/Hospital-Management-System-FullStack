from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

# Config
app.config.from_object('app.config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db.init_app(app)
migrate.init_app(app, db)
api = Api(app)

# Import routes
from .routes.patients import HomeResource, Patient_List, Patient_By_ID, PatientMedicalRecords
from .routes.medical_records import MedicalRecords, MedicalRecordByID
from .routes.departments import DepartmentByID, DepartmentList
from .routes import appointments, departments, doctors, patients, medical_records
from . import models

# Register API resources
api.add_resource(HomeResource, '/')
api.add_resource(Patient_List, '/patients/')
api.add_resource(Patient_By_ID, '/patients/<int:id>')
api.add_resource(PatientMedicalRecords, '/patients/<int:id>/records')
api.add_resource(MedicalRecords, '/records/')
api.add_resource(MedicalRecordByID, '/records/<int:id>')
api.add_resource(DepartmentList, '/departments/')
api.add_resource(DepartmentByID, '/departments/<int:id>')

# Register Blueprints
app.register_blueprint(doctors.doctor_bp)
app.register_blueprint(appointments.appointment_bp)
# app.register_blueprint(departments.department_bp)
# app.register_blueprint(medical_records.record_bp)

# For development ONLY (not for production)
with app.app_context():
    db.create_all()

# Optional main runner
if __name__ == "__main__":
    app.run(debug=True, port=5000)
