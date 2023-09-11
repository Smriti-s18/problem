from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import logout_user
from flask_login import current_user
from flask import flash
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'smriti'


# MySQL Configuration (change these settings to match your MySQL setup)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="smriti2005",
  database="college"
)
cur=mydb.cursor()# Your MySQL database name
#mysql = MySQL(app)
# Route to display list of farmers
@app.route('/farmers')
def farmers():
    cur = mydb.cursor()
    cur.execute('SELECT * FROM farmers')
    farmers_data = cur.fetchall()
    print(farmers_data)
    cur.close()  
    return render_template('farm.html', farmers=farmers_data)

@app.route('/page1')
def page1():
      # Redirect to dashboard if logged in
    return render_template('page1.html')
@app.route('/page')
def index():
    #if current_user.is_authenticated:
        #return redirect(url_for('p'))  # Redirect to dashboard if logged in
    return render_template('index.html')
#app.config['SECRET_KEY'] = 'smriti'
login_manager = LoginManager(app)

# Sample user data
users = {}  # You can manage user data using a dictionary or any other data structure

# User class for Flask-Login
class User(UserMixin):
    pass

# User loader function for Flask-Login



'''from flask import request

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    # Initialize variables
    temperature = None
    weather_description = None
    city_name = None  # Define city_name here

    if request.method == 'POST':
        city_name = request.form.get('city_name')
        print(f'City Name: {city_name}')

    # Fetch weather data using the OpenWeatherMap API
    api_key = '3987515811ef2f98660d11dc80546b60'  # Replace with your OpenWeatherMap API key
    country_code = 'IN'

    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}'
    response = requests.get(base_url)

    if response.status_code == 200:
        weather_data = json.loads(response.text)
        temperature = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        print(f'Temperature: {temperature}°C')
        print(f'Weather Description: {weather_description}')

    else:
        print(f'API Request Failed - Status Code: {response.status_code}')

    # Pass weather data and city as context to the weather.html template
    return render_template('weather.html', temperature=temperature, weather_description=weather_description, city=city_name)

'''
from flask import request, render_template
import requests
import json

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    # Initialize variables
    temperature_fahrenheit = None
    temperature_unit = None
    weather_description = None
    city_name = None

    if request.method == 'POST':
        city_name = request.form.get('city_name')
        print(f'City Name: {city_name}')

    # Fetch weather data using the OpenWeatherMap API
    api_key = '3987515811ef2f98660d11dc80546b60'  # Replace with your OpenWeatherMap API key
    country_code = 'IN'

    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}'
    response = requests.get(base_url)

    if response.status_code == 200:
        weather_data = json.loads(response.text)

        # Check if the API provides temperature in Kelvin or Fahrenheit
        if 'main' in weather_data and 'temp' in weather_data['main']:
            temperature_kelvin = weather_data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15  # Convert to Celsius
            temperature_fahrenheit = (temperature_celsius * 9/5) + 32  # Convert to Fahrenheit
            temperature_unit = "°C"
        else:
            temperature_fahrenheit = weather_data['main']['temp_fahrenheit']
            temperature_unit = "°F"

        weather_description = weather_data['weather'][0]['description']
        print(f'Temperature: {temperature_fahrenheit:.2f}{temperature_unit}')  # Display with appropriate unit
        print(f'Weather Description: {weather_description}')

    else:
        print(f'API Request Failed - Status Code: {response.status_code}')

    # Pass weather data and city as context to the weather.html template
    return render_template('weather.html', temperature=temperature_fahrenheit, temperature_unit=temperature_unit, weather_description=weather_description, city=city_name)





@app.route('/login', methods=['GET', 'POST'])
def login():
    login_successful = False  # Initialize the login status variable
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Replace 'customer' with your table name in the database
        cur = mydb.cursor(dictionary=True)
        cur.execute('SELECT * FROM customer WHERE username = %s', (username,))
        user_data = cur.fetchone()
        cur.close()

        if user_data and 'password' in user_data:
            # Check if the provided password matches the stored password
            if user_data['password'] == password:
                user = User()
                user.id = username
                user.type = user_data['username']  # Assuming you have a 'username' column in your customer table
                login_user(user)
                login_successful = True  # Set login status to True when login is successful
                return redirect(url_for('page1'))
        
        # If the username or password is incorrect, set login status to False
        login_successful = False

    return render_template('login.html', login_successful=login_successful)


# ... Previous code ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Execute registration query
        cur = mydb.cursor()
        cur.execute('INSERT INTO customer (username, password) VALUES (%s, %s)', (username, password))
        mydb.commit()
        cur.close()

        # Redirect to the customer dashboard after successful registration
        return redirect(url_for('page1'))

    return render_template('register.html')

# ... Rest of the code ...
class User(UserMixin):
    def __init__(self, user_id, user_type):
        self.id = user_id
        self.type = user_type
    
    def get_id(self):
        return self.id


# Define the User class for Flask-Login
class User(UserMixin):
    pass

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Load the user object based on the user_id
    # Return the user object or None if not found
    user = User()
    user.id = user_id
    # Load additional user data as needed
    return user


@app.route('/buyers')
def buyers():
    cur = mydb.cursor()
    cur.execute('SELECT * FROM farmers')
    farmers_data = cur.fetchall()
    cur.close()  
    return render_template('buyers.html', farmers=farmers_data)
@app.route('/restaurants')
def restaurants():
    cur = mydb.cursor()
    cur.execute('SELECT * FROM farmers')
    farmers_data = cur.fetchall()
    cur.close()  
    return render_template('restaurants.html', farmers=farmers_data)
@app.route('/foodbanks')
def food_banks():
    # Assuming you have a table named 'food_banks' in your database
    cur = mydb.cursor()
    cur.execute('SELECT * FROM food_banks')
    food_banks_data = cur.fetchall()
    cur.close()  
    return render_template('food_banks.html', food_banks=food_banks_data)


# Sample user data
users = {'user1': {'password': 'pass1', 'type': 'farmer'},
         'user2': {'password': 'pass2', 'type': 'restaurant'}}

class User(UserMixin):
    pass



@app.route('/farmers')
def farm():
    # Your customer-related code here
    return render_template('farm.html')

from flask import render_template

from flask import render_template

@app.route('/customer')
def customer():
    # Sample data for multiple customers
    customers = [
        {
            'name': 'John Doe',
            'phone': '123-456-7890',
            'purchase_history': [
                {'order': 'Apples', 'price': 10, 'date': '2023-09-10'},
                {'order': 'Bananas', 'price': 8, 'date': '2023-09-11'},
                # Add more purchase history items as needed
            ],
        },
        {
            'name': 'Jane Smith',
            'phone': '987-654-3210',
            'purchase_history': [
                {'order': 'Oranges', 'price': 12, 'date': '2023-09-12'},
                {'order': 'Grapes', 'price': 15, 'date': '2023-09-13'},
                # Add more purchase history items as needed
            ],
        },
        # Add more customer data as needed
    ]

    return render_template('customer.html', customers=customers)


@app.route('/cropdisease')
def cropdisease():
    # Your customer-related code here
    return render_template('cropdisease.html')




if __name__ == '__main__':
    app.run(debug=True)
