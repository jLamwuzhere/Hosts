from flask_app import app

#remember to import controllers
from flask_app.controllers import host_controller, rental_controller

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)