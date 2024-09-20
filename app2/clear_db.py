from app import app, db, User, Transaction


def clear_database():
    try:
        db.session.query(Transaction).delete()
        db.session.query(User).delete()

        db.session.commit()
        print("База даних очищена успішно.")
    except Exception as e:
        db.session.rollback()
        print(f"Помилка під час очищення бази даних: {e}")


if __name__ == "__main__":
    with app.app_context():
        clear_database()
