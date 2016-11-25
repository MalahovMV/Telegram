import Class

def exctractDB():
    pass

def create_new_user():
    pass

if __name__ == '__main__':
    db = exctractDB()
    user = input('Login ')
    password = input('password ')
    if (user, password) in db:
        print('Ok')

    else:
        create_new_user()