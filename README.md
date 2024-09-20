## Project Setup

To get started with this project, follow the steps below:

1. **Clone the repository:**
   ```bash
   git clone git@github.com:dreamxgod/transactions-app.git
   ```
2. **Run project with Docker:**
   ```bash
    docker compose up --build
   ```
3. **Run seed script to fill db with data:**
   ```bash
   cd app2
   ```
   ```bash
   python create_data.py
   ```
3. **Navigate to the Flask Admin:**
   [Admin](http://127.0.0.1:8080/admin/))
   
## Project review

In the Flask Admin there are `Home`, `Users`, `Transactions`, `Statistics` windows. In `Users`, `Transactions` you can see and manage db data, in `Statistics` you can see top transactions, date filter, overview statistic. Additionally there are script to clear db `clear_db.py`.
