def check_reg_password(data:dict):
    if not isinstance(data, dict):
        return False

    password1 = data.get('password1')
    password2 = data.get('password2')
    if password1 == password2:
        return True
    return False


def check_restore_data(data:dict):
    if not isinstance(data, dict):
        return False

    values = data.keys()
    true_list = [
        "hash",
        "password1",
        "password2",
    ]
    for value in true_list:
        if value not in values:
            return False
    return True


def check_register_data(data: dict):
    if not isinstance(data, dict):
        return False

    values = data.keys()
    true_list = [
        "email",
        "password1",
        "password2",
    ]
    for value in true_list:
        if value not in values:
            return False
    return True


def check_authorize_data(data:dict):
    if not isinstance(data, dict):
        return False

    values = data.keys()
    true_list = [
        "email",
        "password",
    ]
    for value in true_list:
        if value not in values:
            return False
    return True

def check_notes(data:dict):
    if not isinstance(data, dict):
        return False

    values = data.keys()
    true_list = [
        "title",
        "description",
        "tags"
    ]
    for value in true_list:
        if value not in values:
            return False
    return True

def check_tags(data:dict):
    if not isinstance (data, dict):
        return False

    values = data.keys()
    true_list = [
        "tags",
    ]
    for value in true_list:
        if value not in values:
            return False
    return True
