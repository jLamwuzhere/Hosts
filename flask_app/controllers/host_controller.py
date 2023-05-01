from flask_app.models.host_model import Host
from flask_app import app, render_template, redirect, request, session, flash, bcrypt

# redirect host to /login_reg
@app.get('/')
def redirect_host():
    return redirect('/hosts/login_reg')

#
@app.get('/hosts/login_reg')
def login_reg():
    return render_template('login_reg.html')

# HOST REGISTRATION FORM TO CREATE A HOST VIA REQUEST.FORM METHOD
@app.post('/hosts/register')
def register_host():
    # check if form is valid
    if not Host.validate_registration(request.form):
        return redirect('/hosts/login_reg')
    # if the form is valid, check to see if
    # they already registered
    found_host = Host.find_by_email(request.form)
    print('------------------TESTING PASSWORD TO VALIDATE---------------------')
    if found_host:
        flash('Email already in database. Please login.', 'email')
        return redirect('/hosts/login_reg')
    # hash password (encrypt with bcrypt)
    hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': hashed,
        'rental_length': request.form['rental_length'],
        'payment_method': request.form['payment_method'],
        'rental_proxy': request.form['rental_proxy'],
        'deposit_required': request.form['deposit_required'],
        'phone': request.form['phone'],
        'website': request.form['website'],
    }
    # register (save) the host
    host_id = Host.save(data)
    # log the host in and save host's id in session
    session['host_id'] = host_id
    return redirect('/rentals')

#Login a host
@app.post('/hosts/login')
def login_host():
    # check if form is valid
    if not Host.validate_login(request.form):
        return redirect('/hosts/login_reg')
    # if the form is valid, check to see if
    # they are registered
    found_host = Host.find_by_email(request.form)
    if not found_host:
        flash('Email not found, please register.', 'log_email')
        return redirect('/hosts/login_reg')
    # if they did register, check if the
    # password is correct
    if not bcrypt.check_password_hash(found_host.password, request.form['password']):
        flash('Invalid credentials. Please check your password.', 'log_password')
        return redirect('/hosts/login_reg')
    # if the password is correct,
    # log them in
    session['host_id'] = found_host.id
    return redirect('/rentals')

# READ one host by id with their rentals
@app.get('/hosts/<int:host_id>')
def one_host_with_rentals(host_id):
    data = {
        'id': host_id
    }
    host = Host.find_by_id_with_rentals(data)
    return render_template('one_host_with_rentals.html', host = host)

# READ one host by id with their rentals
@app.get('/hosts/<int:host_id>/info')
def one_host(host_id):
    data = {
        'id': host_id
    }
    host = Host.find_by_id(data)
    return render_template('one_host.html', host = host)

# process form and UPDATE a host by id
@app.post('/hosts/<int:host_id>/update')
def update_host(host_id):
    data = {
        'id': host_id,
        'name': request.form['name'],
    }
    Host.find_by_id_and_update(data)
    print(f'**** UPDATED - host ID: {host_id} ****')
    return redirect(f'/hosts/{host_id}')

# LOGOUT host
@app.get('/hosts/logout')
def logout():
    session.clear()
    return redirect('/hosts/login_reg')

# DELETE one host by id
@app.get('/hosts/<int:host_id>/delete')
def delete_host(host_id):
    data = {
        'id': host_id
    }
    Host.find_by_id_and_delete(data)
    print(f'**** DELETED - host ID: {host_id} ****')
    return redirect('/hosts')