import Repositories.UserRepository as _userRepo

def hello():
    return "Hello"


def get_users():
    return [1, 2, 3]

def create_user(user):
    user.hash_password()
    _userRepo.create_user(user)