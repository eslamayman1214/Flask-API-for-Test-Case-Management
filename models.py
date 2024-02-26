from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text)
    
class ExecutionResult(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable = False)
    test_asset = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(50))