from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app.models import owner_model, pet_model

class Doctor:

    DB = 'vets_office_schema'
    tables = 'doctors'

    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f'''
                SELECT * FROM {cls.tables};'''
        results = connectToMySQL(cls.DB).query_db(query)
        all_users = []
        if len(results) < 1:
            return False
        for row in results:
            one_user = cls(row)
            all_users.append(one_user)
        return all_users
    
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
    def save(cls, form):
        query = f'''INSERT INTO {cls.tables} (first_name, last_name, email, password) 
                VALUES (  %(first_name)s, %(last_name)s, %(email)s, %(password)s  );'''
        
        pw_hash = bcrypt.generate_password_hash(form['password']).decode('utf-8')
        data = {
            'first_name' : form['first_name'],
            'last_name' : form['last_name'],
            'email' : form['email'],
            'password' : pw_hash
        }

        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = f'''UPDATE {cls.tables} 
                SET first_name = %(first_name)s, 
                    last_name = %(last_name)s, 
                    email = %(email)s,
                    phone_number = %(phone_number)s
                WHERE id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, id):
        query = f'DELETE FROM {cls.tables} WHERE id = %(id)s;'
        data = {'id' : id}
        return connectToMySQL(cls.DB).query_db(query, data)

    # query via email
    @classmethod
    def get_one_email(cls, data):
        query = f'SELECT * FROM {cls.tables} WHERE email = %(email)s;'
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)< 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_email( email ):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            is_valid = False
        return is_valid

    @classmethod
    def password_check(cls, data):
        user = cls.get_one_email(data)
        # check if user password matches
        if bcrypt.check_password_hash(user.password, data['password']):
            return True
        return False
    
    @classmethod
    def registration_check(cls, data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 character long', 'registration')
            is_valid = False
        if any(char.isdigit() for char in data['first_name']):
            flash('First name cannot contain numbers', 'registration')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 character long', 'registration')
            is_valid = False
        if any(char.isdigit() for char in data['last_name']):
            flash('Last name cannot contain numbers', 'registration')
            is_valid = False
        if not cls.validate_email(data):
            flash('Invalid email address! Please check spelling.', 'registration')
            is_valid = False
        elif cls.get_one_email(data):
            flash('Email is already registered', 'registration')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long', 'registration')
            is_valid = False
        if len(data['password']) > 20:
            flash('Please do not use a password longer than 20 characters', 'registration')
            is_valid = False
        if not re.search(r'\d', data['password']) or not re.search(r'[A-Z]', data['password']):
            print ('Password requires at least one Capitol letter and 1 digit')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Password does not match', 'registration')
            is_valid = False
        return is_valid

    @classmethod
    def login_check(cls, data):
        is_valid = True
        if not cls.validate_email(data):
            # incorrect email format
            flash('Invalid email address! Check your spelling', 'login')
            is_valid = False
        elif not cls.get_one_email(data):
            # email not in database
            flash('Invalid email/password combination!', 'login')
            is_valid = False
        elif not cls.password_check(data):
            # invalid password
            flash('Invalid email/password combination!', 'login')
            is_valid = False
        return is_valid

    @classmethod
    def validate_update(cls, data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash('First name must contain at least 3 characters')
            is_valid = False
        if any(char.isdigit() for char in data['first_name']):
            flash('First name cannot contain numbers')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name must contain at least 3 characters')
            is_valid = False
        if any(char.isdigit() for char in data['last_name']):
            flash('Last name cannot contain numbers')
            is_valid = False
        if not cls.validate_email(data):
            flash('Invalid email address!')
            is_valid = False
        email = cls.get_one_email({'email':data['email']})
        if email:
            if int(email.id) != int(data['id']):
                flash('Email is already registered')
                is_valid = False
        #! add phone number validation check
        return is_valid