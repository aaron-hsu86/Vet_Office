from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import owner_model, doctor_model

class Pet:

    DB = 'vets_office_schema'
    tables = 'pets'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner_id = data['owner_id']
        self.doctor_id = data['doctor_id']


    @classmethod
    def staff_get_all(cls):
        query = f'''
                SELECT * FROM {cls.tables}
                LEFT JOIN owners ON owners.id = owner_id
                LEFT JOIN doctors ON doctors.id = doctor_id
                ORDER BY owners.id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        all_pets = []
        if len(results) < 1:
            return False
        for row in results:
            one_pet = cls(row)
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
            one_pet.owner = []
            one_pet.owner.append(owner_model.Owner(owner_data))
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
            one_pet.doctor = []
            one_pet.doctor.append(doctor_model.Doctor(doctor_data))
            all_pets.append(one_pet)
        return all_pets
    
    @classmethod
    def user_get_all(cls, id):
        query = f'''
                SELECT * FROM {cls.tables}
                LEFT JOIN owners ON owners.id = owner_id
                WHERE owners.id = %(id)s;'''
        results = connectToMySQL(cls.DB).query_db(query, {'id':id})
        all_pets = []
        if len(results) < 1:
            return False
        for row in results:
            one_pet = cls(row)
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
            one_pet.owner = []
            one_pet.owner.append(owner_model.Owner(owner_data))
            all_pets.append(one_pet)
        return all_pets
    
    @classmethod
    def get_one(cls, id):
        query = f'''
                SELECT * FROM {cls.tables}
                LEFT JOIN owners ON owners.id = owner_id
                WHERE {cls.tables}.id = %(id)s;'''
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        one_pet = cls(results[0])
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
        one_pet.owner = []
        one_pet.owner.append(owner_model.Owner(owner_data))
        return one_pet
    
    @classmethod
    def user_save(cls, data):
        query = f'''INSERT INTO {cls.tables} (name, type, owner_id) 
                VALUES (  %(name)s, %(type)s, %(owner_id)s  );'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def user_update(cls, data):
        query = f'''UPDATE {cls.tables} 
                SET name = %(name)s, 
                    type = %(type)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def doctor_update(cls, data):
        query = f'''UPDATE {cls.tables} 
                SET name = %(name)s, 
                    type = %(type)s, 
                    doctor_id = %(doctor_id)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def validate_update(cls, data):
        is_valid = True
        if len(data['name']) < 2:
            flash('Name must contain at least 2 characters')
            is_valid = False
        if any(char.isdigit() for char in data['name']):
            flash('Name cannot contain numbers')
            is_valid = False
        if len(data['type']) < 3:
            flash('Pet type must be at least 3 characters')
        if any(char.isdigit() for char in data['type']):
            flash('Pet type cannot contain numbers')
            is_valid = False
        return is_valid
    