from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import rental_model
import re # regular expression REGEX

DATABASE = 'hosts_and_rentals_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$')
WEBSITE_REGEX = re.compile(r'^(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)')

class Host:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.rental_length = data['rental_length']
        self.payment_method = data['payment_method']
        self.rental_proxy = data['rental_proxy']
        self.deposit_required = data['deposit_required']
        self.phone = data['phone']
        self.website = data['website']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rentals = []
    
    def __repr__(self):
        return f'<Host: {self.name}>'
    
    @staticmethod
    def validate_registration(form):
        is_valid = True
        if len(form['name']) < 2:
            flash('name must be at least two characters', 'name')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email', 'email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters', 'password')
            is_valid = False
        if form['password'] != form['confirm_password']:
            flash('Passwords must match', 'confirm_password')
            is_valid = False
        if (form['rental_length']) =="choose":
            flash('Please make a lease term selection', 'rental_length')
            is_valid = False
        if len(form['payment_method']) < 1:
            flash('Please select at least one payment method', 'payment_method')
            is_valid = False
        if (form['rental_proxy']) =="choose":
            flash('Please choose an option', 'rental_proxy')
            is_valid = False
        if len(form['deposit_required']) < 1:
            flash('Please enter a deposit amount. If no deposit put 0', 'deposit_required')
            is_valid = False
        if not PHONE_REGEX.match(form['phone']):
            flash('Please enter a valid phone', 'phone')
            is_valid = False
        if len(form['website']) >= 1 and not WEBSITE_REGEX.match(form['website']):
            flash('Please enter a valid website', 'website')
            is_valid = False
        else:
            if len(form['website']) < 1:
                Host.website = "none given"
        return is_valid

    @staticmethod
    def validate_login(form):
        is_valid = True
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email', 'log_email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Password must be at least eight characters', 'log_password')
            is_valid = False
        return is_valid
    
    # find a host by email
    @classmethod
    def find_by_email(cls, data):
        query = 'SELECT * FROM hosts WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Host(results[0])
        return None
    
    # find one host by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * FROM hosts WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Host(results[0])
        return None
    
    @classmethod
    def find_by_id_with_rentals(cls, data):
        query = 'SELECT * FROM hosts JOIN rentals ON hosts.id = rentals.host_id WHERE hosts.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        if len(results) > 0:
            host = Host(results[0])

            for result in results:
                rental_data = {
                    'id': result['rentals.id'],
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
                rental = rental_model.Rental(rental_data)
                host.rentals.append(rental)
        return host
    
    @classmethod
    def save(cls, data):
        query = 'INSERT into hosts (name, email, password, rental_length, payment_method, rental_proxy, deposit_required, phone, website) VALUES (%(name)s, %(email)s, %(password)s, %(rental_length)s, %(payment_method)s, %(rental_proxy)s, %(deposit_required)s, %(phone)s, %(website)s);'
        host_id = connectToMySQL(DATABASE).query_db(query, data)
        print(f'Created: <Host {host_id}>')
        return host_id
    
    # find all hosts (no data needed)
    @classmethod
    def find_all_hosts(cls):
        query = 'SELECT * from hosts;'
        results = connectToMySQL(DATABASE).query_db(query)
        hosts = []
        for result in results:
            hosts.append(Host(result))
        return hosts
    
    # update one host by id
    @classmethod
    def find_host_by_id_and_update(cls, data):
        query = 'UPDATE hosts SET hostname = %(hostname)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one host by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM hosts WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True