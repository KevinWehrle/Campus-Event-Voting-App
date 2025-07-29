from flask import Flask
from flask_cors import CORS
import mysql.connector
from routes import create_routes

app = Flask(__name__)
app.secret_key = 'voting_app_secret'  # Needed for Flask's secure cookie sessions
CORS(app, supports_credentials=True)

# Connect to MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='NaplesF2005!',
    database='CampusVoteDB'
)

# Register blueprint routes
create_routes(app, db)

if __name__ == '__main__':
    app.run(debug=True)
