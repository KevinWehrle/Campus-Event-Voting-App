import mysql.connector
from werkzeug.security import generate_password_hash

# Connect to MySQL
db = mysql.connector.connect(host='localhost', user='root', password='your_password_here')
cursor = db.cursor()

# Create new database
cursor.execute("CREATE DATABASE IF NOT EXISTS CampusVoteDB")
cursor.execute("USE CampusVoteDB")

# Students Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        StudentID INT PRIMARY KEY,
        Password LONGTEXT NOT NULL
    )
""")

students = [
    (10001, "PasswordOne!"),
    (10002, "SecurePass123"),
    (10003, "MyPassword$45")
]

for sid, plain_pw in students:
    hashed = generate_password_hash(plain_pw)
    cursor.execute("INSERT INTO Students (StudentID, Password) VALUES (%s, %s)", (sid, hashed))

# Proposals Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Proposals (
        ProposalID INT PRIMARY KEY,
        Title VARCHAR(200) NOT NULL,
        Description TEXT
    )
""")

proposals = [
    (1, "New Gym Construction", "Proposal to build a new gym facility."),
    (2, "Extended Library Hours", "Proposal to extend library hours till midnight."),
    (3, "Eco-Friendly Campus", "Proposal to add more recycling bins and promote sustainability.")
]

for pid, title, desc in proposals:
    cursor.execute("INSERT INTO Proposals (ProposalID, Title, Description) VALUES (%s, %s, %s)", (pid, title, desc))

# Votes Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Votes (
        VoteID INT AUTO_INCREMENT PRIMARY KEY,
        StudentID INT,
        ProposalID INT,
        UNIQUE(StudentID, ProposalID)  -- ensures one vote per proposal per student
    )
""")

db.commit()
cursor.close()
db.close()
