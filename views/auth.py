#python libraries
import bcrypt

class AuthHandler:
    def __init__(self) -> None:
        pass

    def check_credentials(self, results, login_dict):
        for find in results:
            if find["email"] == login_dict["email"] and bcrypt.checkpw(login_dict["password"].encode('utf-8'), find["password"].encode('utf-8')):
                return True
        return False
