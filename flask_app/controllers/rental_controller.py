from pprint import pprint
from flask_app import app, render_template, redirect, request, session
from flask_app.models.rental_model import Rental
from flask_app.models.host_model import Host

# display form to create a rental
@app.get('/rentals/new')
def new_rental():
    if not 'host_id' in session:
        return redirect('/hosts/login_reg')
    return render_template('new_rental.html')

# process form and create a rental
@app.post('/rentals')
def create_rental():
    if not Rental.validate_rental_form(request.form):
        return redirect('/rentals/new')
    rental_id = Rental.save(request.form)
    print(f'**** CREATED - RENTAL ID: {rental_id} ****')
    return redirect('/rentals')

# # display all rentals only if logged in
# @app.get('/rentals')
# def all_rentals():
#     if not 'host_id' in session:
#         return redirect('/hosts/login_reg')
#     rentals = Rental.find_all_with_hosts()
#     print(f'**************** FOUND - ALL RENTALS: *******************')
#     pprint(rentals)
#     data = {
#         'id': session['host_id']
#     }
#     host= Host.find_by_id(data)
#     return render_template('all_rentals.html', rentals = rentals, host = host)

# display all rentals with user allowed to see not logged in
@app.get('/rentals')
def all_rentals():
    rentals = Rental.find_all_with_hosts()
    if not 'host_id' in session:
        return render_template('all_rentals_not_logged.html', rentals = rentals)
    print(f'**************** FOUND - ALL RENTALS: *******************')
    pprint(rentals)
    data = {
        'id': session['host_id']
    }
    host= Host.find_by_id(data)
    return render_template('all_rentals.html', rentals = rentals, host = host)


# display one rental by id
@app.get('/rentals/<int:rental_id>')
def one_rental(rental_id):
    data = {
        'id': rental_id
    }
    rental = Rental.find_by_id_with_host(data)
    print(f'**** FOUND - RENTAL ID: {rental.id} ****')
    return render_template('one_rental.html', rental = rental)

# display form to edit an rental by id
@app.get('/rentals/<int:rental_id>/edit')
def edit_rental(rental_id):
    if not 'host_id' in session:
        return redirect('/hosts/login_reg')
    data = {
        'id': rental_id
    }
    rental = Rental.find_by_id_with_host(data)
    print(f'**** FOUND - RENTAL ID: {rental.id} ****')
    return render_template('edit_rental.html', rental = rental)

# process form and update an rental by id
@app.post('/rentals/<int:rental_id>/update')
def update_rental(rental_id):
    Rental.find_by_id_and_update(request.form)
    print(f'**** UPDATED - RENTAL ID: {rental_id} ****')
    return redirect(f'/rentals/{rental_id}')

# delete one rental by id
@app.get('/rentals/<int:rental_id>/delete')
def delete_rental(rental_id):
    if not 'host_id' in session:
        return redirect('/hosts/login_reg')
    data = {
        'id': rental_id
    }
    Rental.find_by_id_and_delete(data)
    print(f'**** DELETED - RENTAL ID: {rental_id} ****')
    return redirect('/rentals')