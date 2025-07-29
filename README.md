# Campus Event Voting App

A full-stack voting system that allows college students to log in, vote on campus proposals, and even pitch their own ideas — built using Python, Flask, Tkinter, and MySQL.

---

## Contents

- 'setup_database.py': Sets up MySQL database with tables and sample data
- 'app.py': Flask backend application
- 'routes.py': API endpoints for login, proposals, voting, pitching
- 'client_gui.py': Tkinter GUI client for students
- 'README.md' Project Documentaion

## Setup Instructions

- To be safe, run all files in dedicated terminals!

### 1. Configure the Database

- *Important!* - replace this line with your actual MySQL password:

password='your_password_here'

- Make sure MySQL is running on your machine. Then run:

setup_database.py

- This will create the CampusVoteDB database, add Students, Proposals, and Votes tables, and insert a few sample student users and proposals

### 2. Run the routes

- Run the routes file
  
routes.py

### 3. Start the Flask Backend

- Run the backend server:

app.py

### 4. Launch the GUI Client

- Run the GUI interface:

client_gui.py

## Features

- Log in as a student
- View all active proposals
- Vote on proposals
- Pitch your own proposals

## Security and Features

- Passwords are hashed using werkzeug.security
- Only one vote per student per proposal (enforced in database)
- Used Flask session cookies to track login
- GUI only allows proposal pitching after successful login

## Sample Logins

Use one of these logins to test the app:
- Student ID: 10001 -- Password: PasswordOne!
- Student ID: 10002 -- Password: SecurePass123
- Student ID: 10003 -- Password: MyPassword$45

## Built With

- Python
- Flask
- MySQL
- Tkinter
- Werkzeug Security
