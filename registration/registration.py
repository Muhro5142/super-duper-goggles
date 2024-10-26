import sqlite3

DB_NAME = 'users.db'

def create_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_user(username, email, password):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        return cursor.fetchone() is not None

def display_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, email FROM users')
        for user in cursor.fetchall():
            print(f"Логин: {user[0]}, Электронная почта: {user[1]}")


def user_choice():
    print("\n1. Авторизоваться")
    print("2. Зарегистрироваться")
    choice = input("Введите ваш выбор (1/2): ")
    return choice

def main():
    create_db()
    display_users()  # Показать список пользователей перед выбором действия

    choice = user_choice()

    if choice == '1':
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        if authenticate_user(username, password):
            print("Авторизация успешна.")
        else:
            print("Неверный логин или пароль.")
    elif choice == '2':
        username = input("Введите логин нового пользователя: ")
        email = input("Введите адрес электронной почты нового пользователя: ")
        password = input("Введите пароль нового пользователя: ")
        add_user(username, email, password)
    else:
        print("Неверный ввод. Пожалуйста, введите 1 для авторизации или 2 для регистрации.")

if __name__ == "__main__":
    main()
