from bcrypt import hashpw, gensalt, checkpw

class Hasher:
    @staticmethod
    def hash_password(password):
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
