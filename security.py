# import re

from werkzeug.security import safe_str_cmp

from user import User


# users = [
#     User(1, 'bob', 'asdf'), User(2, 'budhitha', '1234')
# ]
#
# username_mapping = {re.findall(r'[\w\d]+', str(u.username))[0]: u for u in users}
#
# userid_mapping = {int(re.findall(r'[\d]+', str(u.id))[0]): u for u in users}


def authenticate(username, password):
    user = User.find_by_username(username)
    # user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id[0])
    # return userid_mapping.get(user_id[0], None)
