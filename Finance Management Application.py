import mysql.connector

# Create the database if it doesn't exist
conn_init = mysql.connector.connect(
    host="localhost",
    user="TechTalesWithHarsh",
    password="*****************"
)
cursor_init = conn_init.cursor()
cursor_init.execute("CREATE DATABASE IF NOT EXISTS finance_db;")
conn_init.commit()
cursor_init.close()
conn_init.close()

# Connect to the finance_db database
conn = mysql.connector.connect(
    host="localhost",
    user="TechTalesWithHarsh",
    password="@DPMA_gamc_128",
    database="finance_db"
)
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(50), password VARCHAR(50))")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        username VARCHAR(50),
        ttype VARCHAR(10),
        amount FLOAT,
        category VARCHAR(20),
        tdate DATE
    )
""")

def register():
    try:
        print("----- Register -----")
        uname = input("Username: ")
        pwd = input("Password: ")
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, pwd))
        conn.commit()
        print("You are registered!")
    except mysql.connector.Error as e:
        print("Error registering:", e)

def login():
    try:
        print("----- Login -----")
        uname = input("Username: ")
        pwd = input("Password: ")
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
        if cursor.fetchone():
            print("Login successful!")
            return uname
        else:
            print("Wrong details!")
            return None
    except mysql.connector.Error as e:
        print("Error logging in:", e)
        return None

def add_transaction(user):
    try:
        print("----- Add Transaction -----")
        typ = input("Type (income/expense): ")
        amt = float(input("Amount: "))
        cat = input("Category: ")
        date = input("Date (YYYY-MM-DD): ")
        cursor.execute(
            "INSERT INTO transactions (username, ttype, amount, category, tdate) VALUES (%s, %s, %s, %s, %s)",
            (user, typ, amt, cat, date)
        )
        conn.commit()
        print("Transaction added.")
    except mysql.connector.Error as e:
        print("Error adding transaction:", e)

def show_report(user):
    try:
        print("----- Report -----")
        cursor.execute(
            "SELECT ttype, SUM(amount) FROM transactions WHERE username=%s GROUP BY ttype", (user,)
        )
        rows = cursor.fetchall()
        for row in rows:
            print(f"{row[0].capitalize()} : {row[1]}")
        print("------------------")
    except mysql.connector.Error as e:
        print("Error showing report:", e)

def main():
    print("Welcome to Personal Finance Manager!")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                while True:
                    print("1. Add Transaction")
                    print("2. Show Report")
                    print("3. Logout")
                    op = input("Pick one: ")
                    if op == "1":
                        add_transaction(user)
                    elif op == "2":
                        show_report(user)
                    elif op == "3":
                        break
        elif choice == "3":
            break
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()


