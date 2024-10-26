import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users



@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:



def test_add_user_exist():
    
    
    user = 'testuser'
    assert not add_user(username=user , email="testuser@example.com" , password = "password123") 

def test_authenticate_user():
    assert authenticate_user(username="testuser",password="password123")
    assert not authenticate_user(username="fsfgsgdfgf",password="abracadabra")
    assert not authenticate_user(username="testuser",password="abracadabra")
def test_display_users(capsys):
    display_users()
    captured = capsys.readouterr()
    
    # Ожидаемый вывод для двух пользователей
    expected_output = (
        "Логин: testuser, Электронная почта: testuser@example.com\n"
        "Логин: user1, Электронная почта: user1@mail.ru\n"
    )
    
    # Выводим фактический и ожидаемый результат для сравнения
    print("Actual Output:\n", captured.out)
    print("Expected Output:\n", expected_output)
    
    assert captured.out == expected_output
# """
# Тест добавления пользователя с существующим логином.
# Тест успешной аутентификации пользователя.
# Тест аутентификации несуществующего пользователя.
# Тест аутентификации пользователя с неправильным паролем.
# Тест отображения списка пользователей.
# """