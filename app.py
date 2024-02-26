import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from models import db, TestCase, ExecutionResult
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# Get the absolute path to the database file
base_dir = Path(__file__).resolve().parent
db_file_path = os.path.join(base_dir, 'db', 'test_case_management.db')

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this in production

# Initialize SQLAlchemy
db.init_app(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)

jwt = JWTManager(app)

users = {
    'admin' : 'password'
}

#authentication endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        if users.get(username) != password:
            return jsonify({'error': 'Invalid username or password'}), 401
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return render_template('login.html')

# create new test case endpoint
@app.route('/testcases', methods=['POST'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def create_test_case():
    data = request.json
    # validation
    if 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_test_case = TestCase(name=data['name'], description=data['description'])
    db.session.add(new_test_case)
    db.session.commit()
    return jsonify({'message': 'Test case created successfully'}), 201

# retrieving list of all test cases endpoint
@app.route('/testcases', methods=['GET'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def get_all_test_cases():
    test_cases = TestCase.query.all()
    results = [
        {
            'id': test_case.id,
            'name': test_case.name,
            'description': test_case.description
        }
        for test_case in test_cases
    ]
    return jsonify(results), 200

# retrieve single test case by its Id endpoint
@app.route('/testcases/<int:test_case_id>', methods=['GET'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def get_test_case_by_id(test_case_id):
    test_case = TestCase.query.get(test_case_id)
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    result = {
        'id': test_case.id,
        'name': test_case.name,
        'description': test_case.description
    }
    return jsonify(result), 200

# update a test case endpoint
@app.route('/testcases/<int:test_case_id>', methods=['PUT'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def update_test_case(test_case_id):
    test_case = TestCase.query.get(test_case_id)
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    data = request.json
    if 'name' in data:
        test_case.name = data['name']
    if 'description' in data:
        test_case.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Test case updated successfully'}), 200

# delete a test case by its Id endpoint
@app.route('/testcases/<int:test_case_id>', methods=['DELETE'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def delete_test_case(test_case_id):
    test_case = TestCase.query.get(test_case_id)
    if not test_case:
        return jsonify({'error': 'Test case not found'}), 404
    db.session.delete(test_case)
    db.session.commit()
    return jsonify({'message': 'Test case deleted successfully'}), 200

# record execution result for a test case endpoint
@app.route('/executionresults', methods=['POST'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def record_execution_result():
    data = request.json
    if 'test_case_id' not in data or 'test_asset' not in data or 'result' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_execution_result = ExecutionResult(
        test_case_id=data['test_case_id'],
        test_asset=data['test_asset'],
        result=data['result']
    )
    db.session.add(new_execution_result)
    db.session.commit()
    return jsonify({'message': 'Execution result recorded successfully'}), 201

#retrieving the execution results of all test cases for a specific test asset endpoint
@app.route('/executionresults/<string:test_asset>', methods=['GET'])
@jwt_required()  # comment this line to can check functionality without Authentication 
def get_execution_results_by_test_asset(test_asset):
    execution_results = ExecutionResult.query.filter_by(test_asset=test_asset).all()
    if not execution_results:
        return jsonify({'error': 'No execution results found for the specified test asset'}), 404
    results = [
        {
            'id': result.id,
            'test_case_id': result.test_case_id,
            'test_asset': result.test_asset,
            'result': result.result
        }
        for result in execution_results
    ]
    return jsonify(results),200

if __name__ == "__main__":
    app.run(debug= True)