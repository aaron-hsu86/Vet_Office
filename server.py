from flask_app import app
from flask_app.controllers import client_controller, staff_controller

# RUN pipenv install flask pymysql flask-bcrypt

if __name__ == "__main__":
    app.run(debug=True)