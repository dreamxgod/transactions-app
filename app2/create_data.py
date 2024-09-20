import requests
from faker import Faker
import random


BASE_URL = "http://127.0.0.1:8080"
fake = Faker()


def create_sample_data():
    user_ids = []

    for _ in range(5):
        username = fake.user_name()
        response = requests.post(f"{BASE_URL}/add_user", json={"username": username})
        if response.status_code == 200:
            user_id = response.json().get("id")
            user_ids.append(user_id)
        else:
            print(f"Помилка при створенні користувача {username}: {response.text}")

    for user_id in user_ids:
        for _ in range(5):
            amount = random.randint(100, 10000)
            type = fake.word()
            date = fake.date_between(start_date="-30d", end_date="today").strftime(
                "%Y-%m-%d"
            )
            response = requests.post(
                f"{BASE_URL}/add_transaction",
                json={"user_id": user_id, "amount": amount, "type": type, "date": date},
            )
            if response.status_code != 200:
                print(
                    f"Помилка при створенні транзакції для користувача {user_id}: {response.text}"
                )

    print("5 користувачів та по 5 транзакцій для кожного створено успішно.")


if __name__ == "__main__":
    create_sample_data()
