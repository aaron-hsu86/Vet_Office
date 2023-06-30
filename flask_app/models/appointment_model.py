from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import owner_model, doctor_model, pet_model, room_model, appointment_model
from datetime import datetime

class Appointments:

    DB = 'vets_office_schema'
    tables = 'appointments'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.owner_id = data['owner_id']
        self.pet_id = data['pet_id']
        self.doctor_id = data['doctor_id']
        self.room_id = data['room_id']
        self.ETA = data['ETA']
        self.arrival_time = data['arrival_time']
        self.pet_condition = data['pet_condition']
        self.priority = data['priority']
        self.treatment = data['treatment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'''
                SELECT * FROM {cls.tables}
                LEFT JOIN pets ON pet_id = pets.id
                LEFT JOIN owners ON pets.owner_id = owners.id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        all_appointments = []
        if len(results) < 1:
            return False
        for row in results:
            appointment = cls(row)
            pet_data = {
                'id' : row['pets.id'],
                'name' : row['name'],
                'type' : row['type'],
                'created_at' : row['pets.created_at'],
                'updated_at' : row['pets.updated_at'],
                'owner_id' : row['pets.owner_id'],
                'doctor_id' : row['pets.doctor_id']
            }
            appointment.pet = []
            appointment.pet.append(pet_model.Pet(pet_data))
            owner_data = {
                'id':row['owners.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'phone_number':row['phone_number'],
                'created_at':row['owners.created_at'],
                'updated_at':row['owners.updated_at']
            }
            appointment.owner = []
            appointment.owner.append(owner_model.Owner(owner_data))
            all_appointments.append(appointment)
        return all_appointments

    @classmethod
    def get_one(cls, id):
        query = f'''
                SELECT * FROM {cls.tables}
                WHERE id = %(id)s;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        return cls(results[0])
    
    @classmethod
    def user_get_all(cls, id):
        query = f'''
                SELECT * FROM {cls.tables}
                LEFT JOIN pets ON pet_id = pets.id
                LEFT JOIN owners ON pets.owner_id = owners.id
                WHERE {cls.tables}.owner_id = %(id)s;'''
        results = connectToMySQL(cls.DB).query_db(query, {'id':id})
        all_appointments = []
        if len(results) < 1:
            return False
        for row in results:
            appointment = cls(row)
            owner_data = {
                'id':row['owners.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'phone_number':row['phone_number'],
                'created_at':row['owners.created_at'],
                'updated_at':row['owners.updated_at']
            }
            appointment.owner = []
            appointment.owner.append(owner_model.Owner(owner_data))
            pet_data = {
                'id' : row['pets.id'],
                'name' : row['name'],
                'type' : row['type'],
                'created_at' : row['pets.created_at'],
                'updated_at' : row['pets.updated_at'],
                'owner_id' : row['pets.owner_id'],
                'doctor_id' : row['pets.doctor_id']
            }
            appointment.pet = []
            appointment.pet.append(pet_model.Pet(pet_data))
            all_appointments.append(appointment)
        return all_appointments

    @classmethod
    def user_get_one(cls, id):
        query = f'''
                SELECT * FROM {cls.tables}
                WHERE user_id = %(id)s;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        return cls(results[0])

    @classmethod
    def user_save(cls, form):
        query = f'''INSERT INTO {cls.tables} (owner_id, pet_id, ETA, pet_condition) 
                VALUES (  %(owner_id)s, %(pet_id)s, %(ETA)s, %(pet_condition)s  );'''
        data = {
            'owner_id': form['owner_id'],
            'pet_id': form['pet_id'],
            'ETA': datetime.strptime(form['ETA'], '%Y-%m-%dT%H:%M'),
            'pet_condition': form['pet_condition']
        }
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables} 
                SET owner_id = %(owner_id)s, 
                    pet_id = %(pet_id)s, 
                    doctor_id = %(doctor_id)s,
                    room_id = %(room_id)s,
                    ETA = %(ETA)s,
                    arrival_time = %(arrival_time)s,
                    pet_condition = %(pet_condition)s,
                    priority = %(priority)s,
                    treatment = %(treatment)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_user_appointment(form):
        is_valid = True
        if 'pet_id' not in form:
            flash('Please select pet.')
            is_valid = False
        if len(form['ETA']) > 0:
            eta = datetime.strptime(form['ETA'], '%Y-%m-%dT%H:%M')
            if eta < datetime.now():
                flash('Please select future ETA time.')
                is_valid = False
        else:
            flash('Please select ETA time.')
            is_valid = False
        if len(form['pet_condition']) < 3:
            flash('Please put in at least 3 character for condition')
            is_valid = False
        return is_valid
    
    @classmethod
    def validate_user_delete_request(cls, id):
        is_valid = True
        appointment = cls.get_one(id)
        if appointment.owner_id != int(session['id']):
            flash("Please do not delete other people's appointments")
            is_valid = False
        return is_valid

    @classmethod
    def owner_arrived(cls,id):
        query = f'''UPDATE {cls.tables} 
                SET arrival_time = NOW()
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, {'id':id})
    
    @classmethod
    def update_appointment(cls,data):
        query = f'''UPDATE {cls.tables} 
                SET priority = %(priority)s,
                doctor_id = %(doctor_id)s
                WHERE id = %(id)s;'''
        pet_data = {
            'name' : data['pets.name'],
            'type' : data['pets.type'],
            'doctor_id' : data['doctor_id'],
            'id':data['pets.id']
        }
        pet_model.Pet.doctor_update(pet_data)
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update_appointment_room(cls,data):
        query = f'''UPDATE {cls.tables} 
                SET room_id = %(room_id)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def finish_appointment(cls, form):
        query = f'''UPDATE {cls.tables}
                SET pet_condition = %(pet_condition)s,
                    treatment = %(treatment)s
                WHERE id = %(id)s;'''
        data = {
            'pet_condition': form['pet_condition'],
            'treatment': form['treatment'],
            'id':form['id']
        }
        room_model.Rooms.clear_room({'id':form['room_id']})
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def one_pet_history(cls, id):
        query = f'''SELECT * FROM appointments
                    LEFT JOIN pets ON pets.id = pet_id
                    LEFT JOIN owners ON owners.id = pets.owner_id
                    LEFT JOIN doctors ON doctors.id = appointments.doctor_id
                    WHERE appointments.pet_id = %(id)s;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        print(results[0])
        all_history = []
        for row in results:
            one_visit = cls(row)
            pet_data = {
                'id' : row['pets.id'],
                'name' : row['name'],
                'type' : row['type'],
                'created_at' : row['pets.created_at'],
                'updated_at' : row['pets.updated_at'],
                'owner_id' : row['pets.owner_id'],
                'doctor_id' : row['pets.doctor_id']
            }
            one_visit.pet = []
            one_visit.pet.append(pet_model.Pet(pet_data))
            owner_data = {
                'id':row['owners.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'phone_number':row['phone_number'],
                'created_at':row['owners.created_at'],
                'updated_at':row['owners.updated_at']
            }
            one_visit.owner = []
            one_visit.owner.append(owner_model.Owner(owner_data))
            doctor_data = {
                'id':row['doctors.id'],
                'first_name':row['doctors.first_name'],
                'last_name':row['doctors.last_name'],
                'email':row['doctors.email'],
                'password':row['doctors.password'],
                'phone_number':row['doctors.phone_number'],
                'created_at':row['doctors.created_at'],
                'updated_at':row['doctors.updated_at']
            }
            one_visit.doctor = []
            one_visit.doctor.append(doctor_model.Doctor(doctor_data))
            all_history.append(one_visit)
        return all_history