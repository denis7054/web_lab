from doctorapp import db
from datetime import datetime
from sqlalchemy import text
from flask import session, make_response, redirect, url_for, jsonify
import bcrypt

def get_all_requests():
    try:
        result = []  # создаем пустой список
        # Получаем итерируемый объект, где содержатся все строки таблицы contactrequests
        stmt = text("SELECT * FROM sqlite_sequence")
        rows = db.session.execute(stmt).fetchall()
        # Каждую строку конвертируем в словарь
        for row in rows:
            row_dict = dict(row._mapping.items())
            result.append(row_dict)
        # Возвращаем словарь с ключом 'contactrequests', где значение - это список словарей с информацией
        return {'sqlite_sequence': result}
    except Exception as e:
        # Обработка ошибок
        return {'error': str(e)}


# Получаем запрос с фильтром по id
def get_contact_req_by_id(id):
    stmt = text(f"SELECT * FROM contactrequests WHERE id = {id}")
    result = db.session.execute(stmt).fetchone()
    if result:
        return dict(result._asdict())
    else:
        return None
    

    # Получаем список всех запросов.
def get_contact_req_all():
    try:
        result = []  # создаем пустой список
        # Получаем итерируемый объект, где содержатся все строки таблицы contactrequests
        stmt = text("SELECT * FROM contactrequests")
        rows = db.session.execute(stmt).fetchall()
        # Каждую строку конвертируем в словарь
        for row in rows:
            row_dict = dict(row._mapping.items())
            result.append(row_dict)
        # Возвращаем словарь с ключом 'contactrequests', где значение - это список словарей с информацией
        return {'contactrequests': result}
    except Exception as e:
        # Обработка ошибок
        return {'error': str(e)}
    

# Получаем все запросы по имени автора
def get_contact_req_by_author(firstname):
    result = []
    stmt = text(f"SELECT * FROM contactrequests WHERE firstname = '{firstname}'")
    rows = db.session.execute(stmt).fetchall()
    for row in rows:
        row_dict = dict(row._mapping.items())
        result.append(row_dict)
        # result.append(dict(row))
    return {'contactrequests': result}


# Создать новый запрос
def create_contact_req(json_data):
    try:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     # текущая дата и время

        # Используйте text() для объявления текстового SQL-выражения
        stmt = text("INSERT INTO contactrequests (firstname, email, fnum, mess, createdAt, updatedAt) "
                    "VALUES (:firstname, :email, :fnum, :mess, :createdAt, :updatedAt)")

        # Выполните SQL-выражение с использованием параметров
        db.session.execute(stmt, {
            'firstname': json_data['firstname'],
            'email': json_data['email'],
            'fnum': json_data['fnum'],
            'mess': json_data['mess'],
            'createdAt': cur_time,
            'updatedAt': cur_time
        })

        # Подтвердите изменения в БД
        db.session.commit()

        # Возвращаем результат
        return {'message': "ContactRequest Created!"}

    except Exception as e:
        # Откатываем изменения в БД
        db.session.rollback()
        # Возвращаем dict с ключом 'error' и текстом ошибки
        return {'message': str(e)}
    



# Удалить запрос по id в таблице
def delete_contact_req_by_id(id):
    try:
        # DELETE запрос в БД
        stmt = text(f"DELETE FROM contactrequests WHERE id = {id}")
        db.session.execute(stmt)
        db.session.commit()
        return {'message': "ContactRequest Deleted!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

# Обновить текст запроса по id в таблице
def update_contact_req_by_id(id, json_data):
    try:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # текущая дата и время
        # UPDATE запрос в БД
        stmt = text(f"UPDATE contactrequests SET reqtext = '{json_data['mess']}', "f"updatedAt = '{cur_time}' WHERE id = {id}")
        db.session.execute(stmt)
        db.session.commit()
        return {'message': "ContactRequest Updated!"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}
    




# Поиск аккаунта пользователя в БД
def login_user(form_data):
    # Получаем логин и пароль из данных формы
    username = form_data.get('loginField')
    password = form_data.get('passField')
    if username == '':
        return redirect(url_for('login'))
    # Ищем пользователя в БД
    result = db.session.execute(text(f"SELECT * FROM logins WHERE username = '{username}'")).fetchone()
    # если пользователь не найден переадресуем на страницу /login
    if result is None:
        return redirect(url_for('login'))
    # print(result)
    # user = dict(result)
    user = {
        'id': result[0],
        'username': result[1],
        'email': result[2],
        'password': result[3]
    }
    # если пароль не прошел проверку, переадресуем на страницу /login
    if not bcrypt.checkpw(password.encode('utf-8'), user.get('password').encode('utf-8')):
        return redirect(url_for('login'))
    # иначе регистрируем сессию пользователя (записываем логин пользователя в параметр user) и высылаем cookie "AuthToken"
    else:
        response = redirect('/')
        session['user'] = user['username']
        session['userId'] = user['id']
        session['userMail'] = user['email']
        response.set_cookie('AuthToken', user['username'])
        return response


# Создание пользовательского аккаунта
def register_user(form_data):
    # Получаем данные пользователя из формы
    username = form_data.get('loginField')
    password = form_data.get('passField')
    email = form_data.get('emailField')
    # Проверяем полученные данные на наличие обязательных полей
    if username == '' or password == '' or email == '':
        return make_response(jsonify({'message': 'The data entered are not correct!'}), 400)
    # Создаем хеш пароля с солью
    salt = bcrypt.gensalt()
    print(password)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    try:
        stmt = text(f"INSERT INTO logins "
                           f"(username, password, email) "
                           f"VALUES ("
                           f"'{username}', "
                           f"'{hashed}', "
                           f"'{email}'"
                           ")")
        db.session.execute(stmt)
        # Подтверждение изменений в БД
        db.session.commit()
        # Переадресуем на страницу авторизации
        return redirect(url_for('login'))
        # если возникла ошибка запроса в БД
    except Exception as e:
        # откатываем изменения в БД
        db.session.rollback()
        # возвращаем response с ошибкой сервера
        print("Ошибка запроса в БД")
        return make_response(jsonify({'message': str(e)}), 500)