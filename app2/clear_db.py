from app import app, db, User, Transaction

def clear_database():
    try:
        # Видалення всіх записів з таблиці Transaction
        db.session.query(Transaction).delete()
        # Видалення всіх записів з таблиці User
        db.session.query(User).delete()

        # Застосування змін
        db.session.commit()
        print("База даних очищена успішно.")
    except Exception as e:
        # У випадку помилки відмінити зміни
        db.session.rollback()
        print(f"Помилка під час очищення бази даних: {e}")

if __name__ == "__main__":
    # Встановлення контексту застосунку
    with app.app_context():
        clear_database()