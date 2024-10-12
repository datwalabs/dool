import hashlib

class User:
    def __init__(self, user_id: int, username: str, email: str, password: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return (f"User(id={self.user_id}, username='{self.username}', email='{self.email}', "
                f"roles={self.roles})")

class LoginRequest:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class CreateUserRequest:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

    def hash_password(self):
        sha256_hash = hashlib.sha256()
    
        # Update the hash object with the bytes of the password
        sha256_hash.update(self.password.encode('utf-8'))
        
        # Return the hexadecimal representation of the digest
        self.password = sha256_hash.hexdigest()
