import matplotlib.pyplot as plt
import io
import base64
from markupsafe import Markup

# Встановлюємо режим 'Agg' для matplotlib
plt.switch_backend('Agg')

# Функція для створення графіку найбільших транзакцій
def plot_top_transactions(session):
    from app import Transaction, User  # Імпорт всередині функції, щоб уникнути циклічного імпорту

    # Отримати топ-10 транзакцій, відсортованих за спаданням
    transactions = session.query(Transaction).order_by(Transaction.amount.desc()).limit(10).all()
    amounts = [t.amount for t in transactions]
    usernames = [session.query(User).get(t.user_id).username for t in transactions]

    # Побудова графіку
    plt.figure(figsize=(10, 5))
    bars = plt.bar(usernames, amounts)
    plt.xlabel('Username')
    plt.ylabel('Transaction Amount')
    plt.title('Top Transactions')

    # Додавання можливості кліку на імена користувачів
    for bar, transaction in zip(bars, transactions):
        username = session.query(User).get(transaction.user_id).username
        bar.set_picker(True)  # Встановлюємо, що стовпчик можна обирати

    # Збереження графіку в буфер
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

# Функція для відображення графіку в шаблоні
def render_top_transactions(session):
    img_data = plot_top_transactions(session)
    return Markup(f'<img src="data:image/png;base64,{img_data}" style="width:100%;" />')