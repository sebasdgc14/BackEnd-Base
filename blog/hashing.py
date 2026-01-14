from passlib.context import CryptContext


class Hash:
    def scrypt(password: str):
        pwd_cxt = CryptContext(schemes=["scrypt"], deprecated="auto")
        return pwd_cxt.hash(password)
