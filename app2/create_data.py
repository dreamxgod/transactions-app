import requests

# URL вашого застосунку
BASE_URL = "http://127.0.0.1:5000"

def create_sample_data():
    user_ids = []

    # Створення 5 користувачів
    for i in range(5):
        username = f'user{i+1}'
        response = requests.post(f"{BASE_URL}/add_user", json={"username": username})
        if response.status_code == 200:
            user_id = response.json().get('id')
            user_ids.append(user_id)
        else:
            print(f"Помилка при створенні користувача {username}: {response.text}")

    # Додавання 5 транзакцій для кожного користувача
    for user_id in user_ids:
        for j in range(5):
            amount = (j + 1) * 100
            type = f'type{j+1}'
            response = requests.post(f"{BASE_URL}/add_transaction", json={"user_id": user_id, "amount": amount, "type": type})
            if response.status_code != 200:
                print(f"Помилка при створенні транзакції для користувача {user_id}: {response.text}")

    print("5 користувачів та по 5 транзакцій для кожного створено успішно.")

if __name__ == "__main__":
    create_sample_data()
