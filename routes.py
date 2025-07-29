# routes.py
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash  # Use this instead of flask_bcrypt
from mysql.connector import Error

app_routes = Blueprint('app_routes', __name__)

def create_routes(app, db):
    cursor = db.cursor(dictionary=True)

    @app.route('/pitch', methods=['POST'])
    def pitch_proposal():
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"error": "Unauthorized."}), 401

        data = request.get_json()
        title = data.get('title')
        description = data.get('description')

        if not title or not description:
            return jsonify({"error": "Title and description are required."}), 400

        try:
            cursor.execute("INSERT INTO Proposals (Title, Description, PitchedBy) VALUES (%s, %s, %s)",
                       (title, description, f"Student ID: {student_id}"))
            db.commit()
            return jsonify({"message": "Proposal pitched successfully."}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500




    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        student_id = data.get('student_id')
        password = data.get('password')

        try:
            cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (student_id,))
            user = cursor.fetchone()
            if user and check_password_hash(user['Password'], password):
                session['student_id'] = student_id
                return jsonify({"message": "Login successful."}), 200
            else:
                return jsonify({"error": "Invalid credentials."}), 401
        except Error as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()
        return jsonify({"message": "Logged out."}), 200

    @app.route('/proposals', methods=['GET'])
    def get_proposals():
        try:
            cursor.execute("SELECT * FROM Proposals")
            proposals = cursor.fetchall()
            return jsonify(proposals), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/vote/<int:proposal_id>', methods=['POST'])
    def cast_vote(proposal_id):
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({"error": "Unauthorized."}), 401

        try:
            cursor.execute("SELECT * FROM Votes WHERE StudentID = %s AND ProposalID = %s", (student_id, proposal_id))
            if cursor.fetchone():
                return jsonify({"error": "You have already voted for this proposal."}), 409

            cursor.execute("INSERT INTO Votes (StudentID, ProposalID) VALUES (%s, %s)", (student_id, proposal_id))
            db.commit()
            return jsonify({"message": "Vote recorded."}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500

    return app
