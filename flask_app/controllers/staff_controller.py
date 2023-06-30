from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import owner_model, doctor_model, pet_model, appointment_model, room_model

@app.route('/staff_signin')
def staff_login():

    return render_template('staff_login.html')

@app.route('/staff_registration', methods=['post'])
def staff_registration_check():
    if not doctor_model.Doctor.registration_check(request.form):
        return redirect('/staff_signin')
    id = doctor_model.Doctor.save(request.form)
    session['doctor_id'] = id
    return redirect('/staff_dashboard')

@app.route('/staff_login', methods=['post'])
def staff_login_check():
    if not doctor_model.Doctor.login_check(request.form):
        return redirect('/staff_signin')
    id = doctor_model.Doctor.get_one_email(request.form).id
    session['doctor_id'] = id
    return redirect('/staff_dashboard')

#! staff must be logged in past here
@app.route('/staff_dashboard')
def staff_dashboard():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    doctor = doctor_model.Doctor.get_one(session['doctor_id'])
    all_rooms = room_model.Rooms.get_all()
    all_appointments = appointment_model.Appointments.get_all()
    all_doctors = doctor_model.Doctor.get_all()
    # print(all_rooms[0].doctor[0].id)
    return render_template('staff_dashboard.html', doctor=doctor, all_rooms=all_rooms, all_appointments=all_appointments, all_doctors=all_doctors)

@app.route('/staff_account')
def staff_account():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    doctor = doctor_model.Doctor.get_one(session['doctor_id'])
    return render_template('/staff_edit.html', doctor=doctor)

@app.route('/staff_account/edit', methods=['post'])
def staff_account_update():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    doctor = doctor_model.Doctor.get_one(session['doctor_id'])
    if session['doctor_id'] != doctor.id:
        flash('Please do not attempt to edit another doctors information!')
        return redirect('/staff_dashboard')
    if not doctor_model.Doctor.validate_update(request.form):
        return redirect('/staff_account')
    doctor_model.Doctor.update(request.form)
    return redirect('/staff_dashboard')

@app.route('/clients')
def view_all_clients():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    client_pets = pet_model.Pet.staff_get_all()
    return render_template('staff_client_info.html', client_pets=client_pets)

@app.route('/pet_info/<int:id>')
def view_pet_info(id):
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    pet_history = appointment_model.Appointments.one_pet_history(id)
    pet_info = pet_model.Pet.get_one(id)
    return render_template('staff_pet_info.html', pet_info = pet_info, pet_history=pet_history)

@app.route('/create_room', methods=['post'])
def create_room_check():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    if not room_model.Rooms.validate_create(request.form):
        return redirect('/staff_dashboard')
    room_model.Rooms.save(request.form)
    return redirect('/staff_dashboard')

@app.route('/office_arrival/<int:id>')
def office_arrival(id):
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    appointment_model.Appointments.owner_arrived(id)
    return redirect('/staff_dashboard')

@app.route('/move_to_room', methods=['post'])
def move_to_room():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    appointment = appointment_model.Appointments.get_one(request.form['id'])
    room_data = {
        'doctor_id':appointment.doctor_id,
        'pet_id':appointment.pet_id,
        'owner_id':appointment.owner_id,
        'id':request.form['room_id']
    }
    room_model.Rooms.update(room_data)
    print(request.form)
    appointment_model.Appointments.update_appointment_room(request.form)
    return redirect('/staff_dashboard')

@app.route('/update_appointment', methods=['post'])
def update_appointment():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    appointment_model.Appointments.update_appointment(request.form)
    return redirect('/staff_dashboard')

@app.route('/room/<int:id>')
def room_info(id):
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    room_info = room_model.Rooms.get_one(id)
    return render_template('room_checkup.html', room_info = room_info)

@app.route('/diagnosis', methods=['post'])
def give_diagnosis():
    if 'doctor_id' not in session:
        flash('Please login!','user')
        return redirect('/staff_signin')
    print('request form:')
    print(request.form)
    appointment_model.Appointments.finish_appointment(request.form)
    return redirect('/staff_dashboard')