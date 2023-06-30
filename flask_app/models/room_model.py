from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import owner_model, doctor_model, pet_model, appointment_model

class Rooms:

    DB = 'vets_office_schema'
    tables = 'rooms'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.doctor_id = data['doctor_id']
        self.owner_id = data['owner_id']
        self.pet_id = data['pet_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'''
                SELECT * from {cls.tables}
                LEFT JOIN pets ON pets.id = pet_id
                LEFT JOIN owners ON owners.id = pets.owner_id
                LEFT JOIN doctors ON doctors.id = pets.doctor_id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        all_rooms = []
        if len(results) < 1:
            return False
        for row in results:
            one_room = cls(row)
            one_room.pet = []
            pet_data = {
                'id' : row['pets.id'],
                'name' : row['pets.name'],
                'type' : row['type'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at'],
                'owner_id' : row['pets.owner_id'],
                'doctor_id' : row['pets.doctor_id']
            }
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
            one_room.pet.append(pet_model.Pet(pet_data))
            one_room.owner = []
            one_room.owner.append(owner_model.Owner(owner_data))
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
            one_room.doctor = []
            one_room.doctor.append(doctor_model.Doctor(doctor_data))
            all_rooms.append(one_room)
        return all_rooms

    @classmethod
    def get_one(cls, id):
        query = f'''
                SELECT * FROM {cls.tables}
                LEFT JOIN appointments ON rooms.id = room_id
                LEFT JOIN pets ON pets.id = rooms.pet_id
                LEFT JOIN owners ON owners.id = rooms.owner_id
                LEFT JOIN doctors ON doctors.id = rooms.doctor_id
                WHERE {cls.tables}.id = %(id)s AND treatment IS NULL;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        one_room = cls(results[0])
        one_room.appointment = []
        appointment_data ={
            'id' : results[0]['appointments.id'],
            'owner_id' : results[0]['appointments.owner_id'],
            'pet_id' : results[0]['appointments.pet_id'],
            'doctor_id' : results[0]['appointments.doctor_id'],
            'room_id' : results[0]['room_id'],
            'ETA' : results[0]['ETA'],
            'arrival_time' : results[0]['arrival_time'],
            'pet_condition' : results[0]['pet_condition'],
            'priority' : results[0]['priority'],
            'treatment' : results[0]['treatment'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at']
        }
        one_room.appointment.append(appointment_model.Appointments(appointment_data))
        one_room.pet = []
        pet_data = {
            'id' : results[0]['pets.id'],
            'name' : results[0]['pets.name'],
            'type' : results[0]['type'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at'],
            'owner_id' : results[0]['pets.owner_id'],
            'doctor_id' : results[0]['pets.doctor_id']
        }
        owner_data = {
            'id':results[0]['owners.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'phone_number':results[0]['phone_number'],
            'created_at':results[0]['owners.created_at'],
            'updated_at':results[0]['owners.updated_at']
        }
        one_room.pet.append(pet_model.Pet(pet_data))
        one_room.owner = []
        one_room.owner.append(owner_model.Owner(owner_data))
        doctor_data = {
            'id':results[0]['doctors.id'],
            'first_name':results[0]['doctors.first_name'],
            'last_name':results[0]['doctors.last_name'],
            'email':results[0]['doctors.email'],
            'password':results[0]['doctors.password'],
            'phone_number':results[0]['doctors.phone_number'],
            'created_at':results[0]['doctors.created_at'],
            'updated_at':results[0]['doctors.updated_at']
        }
        one_room.doctor = []
        one_room.doctor.append(doctor_model.Doctor(doctor_data))
        return one_room

    @classmethod
    def save(cls, data):
        query = f'''INSERT INTO {cls.tables} (name) 
                VALUES (  %(name)s  );'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables} 
                SET doctor_id = %(doctor_id)s, 
                    pet_id = %(pet_id)s,
                    owner_id = %(owner_id)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls):

        return

    @staticmethod
    def validate_create(data):
        is_valid = True
        if len(data['name']) < 3:
            flash('Name cannot be shorter than 3 characters')
            is_valid = False
        return is_valid

    @classmethod
    def clear_room(cls, id):
        query = f'''UPDATE {cls.tables} 
                SET doctor_id = null,
                    pet_id = null,
                    owner_id = null
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, id)
