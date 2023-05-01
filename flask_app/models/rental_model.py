from pprint import pprint
from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import host_model

DATABASE = 'hosts_and_rentals_schema'

class Rental:
    def __init__(self, data):
        self.id = data['id']
        self.pic = data['pic']
        self.address = data['address']
        self.bedrooms = data['bedrooms']
        self.bathrooms = data['bathrooms']
        self.price = data['price']
        self.duration = data['duration']
        self.date_available = data['date_available']
        self.pet_friendly = data['pet_friendly']
        self.short_term = data['short_term']
        self.bedrooms = data['bedrooms']
        self.description = data['description']
        self.host_id = data['host_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.host = data['host']
    
    def __repr__(self):
        return f'<Rental: {self.address}>'
    
    @staticmethod
    def validate_rental_form(form):
        is_valid = True
        if len(form['pic']) < 2:
            flash('Pic must be at least two characters.', 'pic')
            is_valid = False
        if len(form['address']) < 2:
            flash('Address must be at least two characters.', 'address')
            is_valid = False
        if (form['bedrooms']) =="choose":
            flash('Please choose an option', 'bedrooms')
            is_valid = False
        if (form['bathrooms']) =="choose":
            flash('Please choose an option', 'bathrooms')
            is_valid = False
        if len(form['price']) < 1:
            flash('Please enter a price amount', 'price')
            is_valid = False
        if len(form['duration']) < 2:
            flash('Duration must be at least two characters.', 'duration')
            is_valid = False
        if not form['date_available']:
            flash('Please enter a move-in date.', 'date_available')
            is_valid = False
        if not form['pet_friendly']:
            flash('Please select yes or no.', 'pet_friendly')
            is_valid = False
        if not form['short_term']:
            flash('Please select yes or no.', 'short_term')
            is_valid = False
        if len(form['description']) < 2:
            flash('Description must be at least two characters.', 'description')
            is_valid = False
        return is_valid

    # create a rental
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO rentals (pic, address, bedrooms, bathrooms, price, duration, date_available, pet_friendly, short_term, description, host_id) VALUES (%(pic)s, %(address)s, %(bedrooms)s, %(bathrooms)s, %(price)s, %(duration)s, %(date_available)s, %(pet_friendly)s, %(short_term)s, %(description)s, %(host_id)s);'
        rental_id = connectToMySQL(DATABASE).query_db(query, data)
        return rental_id

    # find all rentals (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from rentals;'
        results = connectToMySQL(DATABASE).query_db(query)
        rentals = []
        for result in results:
            rentals.append(Rental(result))
        pprint(rentals)
        return rentals
    
    # find all rentals with hosts (no data needed)
    @classmethod
    def find_all_with_hosts(cls):
        query = 'SELECT * from rentals JOIN hosts ON rentals.host_id = hosts.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        rentals = []
        for result in results:
            host_data = {
                'id': result['host_id']
            }
            host = host_model.Host.find_by_id(host_data)
            rental_data = {
                'id': result['id'],
                'pic': result['pic'],
                'address': result['address'],
                'bedrooms': result['bedrooms'],
                'bathrooms': result['bathrooms'],
                'price': result['price'],
                'duration': result['duration'],
                'date_available': result['date_available'],
                'pet_friendly': result['pet_friendly'],
                'short_term': result['short_term'],
                'description': result['description'],
                'host_id': result['host_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'host': host
            }
            rental = Rental(rental_data)
            rentals.append(rental)
        return rentals

    # find one rental by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from rentals WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        rental = Rental(results[0])
        return rental
    
    # find one rental by id with host
    @classmethod
    def find_by_id_with_host(cls, data):
        query = 'SELECT * from rentals JOIN hosts ON rentals.host_id = hosts.id WHERE rentals.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        host_data = {
            'id': results[0]['host_id']
        }
        host = host_model.Host.find_by_id(host_data)
        rental_data = {
            'id': results[0]['id'],
            'pic': results[0]['pic'],
            'address': results[0]['address'],
            'bedrooms': results[0]['bedrooms'],
            'bathrooms': results[0]['bathrooms'],
            'price': results[0]['price'],
            'duration': results[0]['duration'],
            'date_available': results[0]['date_available'],
            'pet_friendly': results[0]['pet_friendly'],
            'short_term': results[0]['short_term'],
            'description': results[0]['description'],
            'host_id': results[0]['host_id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'host': host,
        }
        rental = Rental(rental_data)
        return rental

    # update one rental by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE rentals SET pic = %(pic)s, address = %(address)s, bedrooms = %(bedrooms)s, bathrooms = %(bathrooms)s, price = %(price)s, duration = %(duration)s, date_available = %(date_available)s, pet_friendly = %(pet_friendly)s, short_term = %(short_term)s, description = %(description)s, host_id = %(host_id)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one rental by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM rentals WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True