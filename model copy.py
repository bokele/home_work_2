import sqlite3

def show_color(username):
    connection = sqlite3.connect('flask_tut.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT favorivte_color FROM user WHERE username = '{username}' ORDER BY pk DESC; """.format(username = username)
    )

    color = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
    messsage = "{username} 's favorite color is {color}".format(username = username, color = color)
    return messsage

def check_password(username):
    connection = sqlite3.connect('flask_tut.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT password FROM user WHERE username = '{username}'; """.format(username = username)
    )
    password = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()
   
    return password

def login(email,password ):
    connection = sqlite3.connect('flask_tut.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT username,email FROM user WHERE email = '{email}' and password='{password}'; """.format(email = email,password = password)
    )
    db_username = cursor.fetchone()[0]

    if db_username is None:
        connection.commit()
        cursor.close()
        connection.close()
        message = "We did it find a user with this creadition, please try again"
        return message
    
    else:
        message = "Welcom again"
        return db_username



def todolist(user_id):
    connection = sqlite3.connect('flask_tut.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT name FROM todoList WHERE user_id = {user_id} ; """.format(user_id = user_id)
    )
    todolist = cursor.fetchone()[0]

    if todolist is None:
        connection.commit()
        cursor.close()
        connection.close()
        message = "We did it find a user with this creadition, please try again"
        return message
    else:
        return todolist

def signup(username,password ):
    connection = sqlite3.connect('flask_tut.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute(
        """ SELECT username FROM user WHERE username = '{username}'; """.format(username = username)
    )
    db_username = cursor.fetchone()[0]

    if db_username is None:
        favorite_color = "red"
        cursor.execute(
            """ INSERT INTO user INSERT INTO user(username, password, favorivte_color)
            VALUES(
                '{username}',
                '{password}',
                '{favorite_color}'
            );""".format(username = username, password = password, favorivte_color = favorite_color )
        )
        connection.commit()
        cursor.close()
        connection.close()
    else:

        return "User already existed"
    message = "You are seccessfully signed up"
    return message


