from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import owner_model, pet_model, appointment_model

# home/main page
@app.route('/')
def main_page():
    return render_template('login_registration.html')
# Registration checks
@app.route('/registration', methods=['post'])
def registration_check():
    if not owner_model.Owner.registration_check(request.form):
        return redirect('/')
    id = owner_model.Owner.save(request.form)
    session['id'] = id
    return redirect('/dashboard')
# Login checks
@app.route('/login', methods=['post'])
def login_check():
    if not owner_model.Owner.login_check(request.form):
        return redirect('/')
    id = owner_model.Owner.get_one_email(request.form).id
    session['id'] = id
    return redirect('/dashboard')
# Logout
@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')

# Dashboard - #! Needs to be logged in past this point
@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    user = owner_model.Owner.get_one(session['id'])
    all_pets = pet_model.Pet.user_get_all(session['id'])
    all_appointments = appointment_model.Appointments.user_get_all(session['id'])
    # print(all_pets)
    # print(all_appointments[0].arrival_time)
    return render_template('client_dashboard.html', user=user, all_pets=all_pets, all_appointments=all_appointments)

# add pet
@app.route('/add_pet')
def add_pet():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    return render_template('pet_add.html')
# validate add pet
@app.route('/add_pet/check', methods=['post'])
def add_pet_validate():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    if not pet_model.Pet.validate_update(request.form):
        return redirect('/add_pet')
    return redirect('/dashboard')

# edit pet info
@app.route('/edit_pet/<int:id>')
def edit_pet(id):
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    pet = pet_model.Pet.get_one(id)
    if not pet.owner_id == session['id']:
        flash("Please do not attempt to edit other people's pets!")
        return redirect('/dashboard')
    return render_template('pet_edit.html', pet=pet)
# validate pet edit
@app.route('/edit_pet/check', methods=['post'])
def edit_pet_validate():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    if not pet_model.Pet.validate_update(request.form):
        return redirect('/edit_pet')
    pet_model.Pet.user_save(request.form)
    return redirect('/dashboard')

# delete pet info
@app.route('/delete_pet/<int:id>')
def delete_pet(id):
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    pet = pet_model.Pet.get_one(id)
    if not pet.owner_id == session['id']:
        flash("Please do not attempt to edit other people's pets!")
        return redirect('/dashboard')
    pet_model.Pet.delete(id)
    return redirect('/dashboard')

# edit owner info
@app.route('/account')
def edit_owner():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    owner = owner_model.Owner.get_one(session['id'])
    return render_template('owner_edit.html', owner=owner)
@app.route('/account/check', methods=['post'])
def edit_owner_validate():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    owner = owner_model.Owner.get_one(session['id'])
    if session['id'] != owner.id:
        flash('Please do not attempt to edit another owner information!')
        return redirect('/dashboard')
    if not owner_model.Owner.validate_update(request.form):
        return redirect('/account')
    owner_model.Owner.update(request.form)
    return redirect('/dashboard')

# Set up new appointment
@app.route('/new_appointment')
def new_appointment():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    all_pets = pet_model.Pet.user_get_all(session['id'])
    return render_template('appointment_new.html', all_pets=all_pets)
# validate appointment
@app.route('/new_appointment/check', methods=['post'])
def new_appointment_validate():
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    if not appointment_model.Appointments.validate_user_appointment(request.form):
        return redirect('/new_appointment')
    appointment_model.Appointments.user_save(request.form)
    return redirect('/dashboard')

# Delete appoitment?
@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    if not appointment_model.Appointments.validate_user_delete_request(id):
        return redirect('/dashboard')
    appointment_model.Appointments.delete(id)
    return redirect('/dashboard')

@app.route('/appointment_arrival/<int:id>')
def appointment_arrival(id):
    if 'id' not in session:
        flash('Please login!','user')
        return redirect('/')
    appointment_info = appointment_model.Appointments.get_one(id)
    if not (int(session['id']) == appointment_info.owner_id):
        flash("Please do not affect other people's apppointments")
        return redirect('/dashboard')
    appointment_model.Appointments.owner_arrived(id)
    return redirect('/dashboard')