
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://todo_user:1234@localhost:5433/transactions-app2"
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

# Модель User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

# Модель Transaction
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Додали поле type
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

# Ініціалізація Flask-Admin
admin = Admin(app, name='MyApp Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Transaction, db.session))

# Ендпоїнти
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username})

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    transactions = [{"id": t.id, "amount": t.amount, "type": t.type} for t in user.transactions]
    return jsonify({"id": user.id, "username": user.username, "transactions": transactions})

@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        transactions = [{"id": t.id, "amount": t.amount, "type": t.type} for t in user.transactions]
        result.append({"id": user.id, "username": user.username, "transactions": transactions})
    return jsonify(result)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    user_id = request.json.get('user_id')
    amount = request.json.get('amount')
    type = request.json.get('type')
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    transaction = Transaction(amount=amount, type=type, user=user)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"id": transaction.id, "amount": transaction.amount, "type": transaction.type})

# Маршрут для тестування
@app.route('/')
def index():
    return '<h1>Flask Admin App</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
