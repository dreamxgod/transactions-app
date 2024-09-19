import matplotlib.pyplot as plt
import io
import base64
from markupsafe import Markup

# Встановлюємо режим 'Agg' для matplotlib
plt.switch_backend('Agg')

# Функція для створення графіку найбільших транзакцій
def plot_top_transactions(session):
    from app import Transaction  # Імпорт всередині функції, щоб уникнути циклічного імпорту

    # Отримати топ-10 транзакцій
    transactions = session.query(Transaction).order_by(Transaction.amount.desc()).limit(10).all()
    amounts = [t.amount for t in transactions]
    user_ids = [t.user_id for t in transactions]

    # Побудова графіку
    plt.figure(figsize=(10, 5))
    plt.bar(user_ids, amounts)
    plt.xlabel('User ID')
    plt.ylabel('Transaction Amount')
    plt.title('Top 10 Transactions')
    
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