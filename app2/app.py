from flask import Flask, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from some_statistics import render_top_transactions

app = Flask(__name__, template_folder='/Users/ivankalinets/fastapi-transactions-app/app2/ templates')

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://todo_user:1234@localhost:5433/transactions-app2"
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

# Модель Transaction
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

# Кастомний клас UserView для додавання кнопки перегляду транзакцій
class UserView(ModelView):
    # Додати колонку з кнопкою для перегляду транзакцій
    column_formatters = {
        'transactions': lambda v, c, m, p: Markup(f'<a href="{url_for(".transactions_view", user_id=m.id)}">View Transactions</a>')
    }

    column_list = ['id', 'username', 'transactions']

    @expose('/transactions/<int:user_id>/')
    def transactions_view(self, user_id):
        # Отримати користувача за user_id
        user = User.query.get(user_id)
        if user is None:
            return self.render('not_found.html')

        # Отримати всі транзакції користувача
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return self.render('transactions.html', user=user, transactions=transactions)

# Кастомний клас StatisticsView для відображення статистики
class StatisticsView(BaseView):
    @expose('/')
    def index(self):
        top_transactions_chart = render_top_transactions(db.session)  # Передаємо сесію
        return self.render('statistics.html', top_transactions_chart=top_transactions_chart)

    def is_accessible(self):
        # Дозволяємо доступ до сторінки
        return True

# Ініціалізація Flask-Admin
admin = Admin(app, name='MyApp Admin', template_mode='bootstrap3')
admin.add_view(UserView(User, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(StatisticsView(name='Statistics', endpoint='statistics'))  # Додаємо StatisticsView

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
    app.run(debug=True, port=8080)